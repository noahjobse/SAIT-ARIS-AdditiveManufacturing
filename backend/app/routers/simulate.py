"""
POST /api/simulate — full pipeline: MoveCommand[] → trajectory waypoints.

Bridges the frontend's flat MoveCommand list to the internal Program AST,
runs TrajectoryGenerator (IK-backed), and returns timestamped waypoints.
"""
import asyncio
import functools
import logging
import math
import time

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.collision.detector import CollisionDetector
from app.kinematics.solver import KinematicsSolver
from app.parser.ast_nodes import (
    Declaration,
    JointTarget,
    Module,
    MoveCommand,
    Orientation,
    Position,
    Procedure,
    Program,
    RobTarget,
    ToolData,
)
from app.schemas.simulate import (
    CollisionInfo,
    SimulateResponse,
    SimulationStats,
    TCPPose,
    TrajectoryWaypoint,
)
from app.thread_pool import executor, pybullet_lock
from app.trajectory.generator import TrajectoryError, TrajectoryGenerator

router = APIRouter()
logger = logging.getLogger(__name__)

# Shared solver (PyBullet headless) — created once at import time
_solver = KinematicsSolver()
_generator = TrajectoryGenerator(_solver)
_detector = CollisionDetector(loader=_solver.loader)

# ---------------------------------------------------------------------------
# Request schema
# ---------------------------------------------------------------------------

class ObstacleTransform(BaseModel):
    obstacle_id: str
    position: list[float] = [0.0, 0.0, 0.0]
    rotation: list[float] = [0.0, 0.0, 0.0]


class SimulateRequest(BaseModel):
    robot_id: str
    ast: list[dict] = []         # MoveCommand dicts (used when program not provided)
    program: dict | None = None  # Full parse.py program dict (preserves declarations)
    obstacles: list[ObstacleTransform] = []


# ---------------------------------------------------------------------------
# Bridge: frontend MoveCommand dict → Python dataclass
# ---------------------------------------------------------------------------

def _build_robtarget(target: dict) -> RobTarget:
    """
    Convert a RobTarget dict to the Python dataclass.

    Handles two formats:
    - parse.py output: { position: {x,y,z}, orientation: {q1,q2,q3,q4} }
    - OpenAPI schema:  { type: "RobTarget", trans: [x,y,z], rot: [q1,q2,q3,q4] }
    """
    if "position" in target:
        # Python dataclass dict (from parse.py _to_dict)
        p = target["position"]
        r = target["orientation"]
        return RobTarget(
            position=Position(x=p["x"], y=p["y"], z=p["z"]),
            orientation=Orientation(q1=r["q1"], q2=r["q2"], q3=r["q3"], q4=r["q4"]),
        )
    # OpenAPI schema format (trans array, rot array)
    trans = target.get("trans", [0.0, 0.0, 0.0])
    rot = target.get("rot", [1.0, 0.0, 0.0, 0.0])
    return RobTarget(
        position=Position(x=trans[0], y=trans[1], z=trans[2]),
        orientation=Orientation(q1=rot[0], q2=rot[1], q3=rot[2], q4=rot[3]),
    )


def _build_jointtarget(target: dict) -> JointTarget:
    return JointTarget(
        robot_axes=target.get("robot_axes", [0.0] * 6),
        external_axes=target.get("external_axes", [0.0] * 6),
    )


def _build_target(target: dict) -> RobTarget | JointTarget:
    """Detect and convert a target dict, supporting both dict formats."""
    # Python dataclass dict has 'robot_axes' key for JointTarget
    if "robot_axes" in target:
        return _build_jointtarget(target)
    # OpenAPI schema uses 'type' discriminator
    if target.get("type") == "JointTarget":
        return _build_jointtarget(target)
    return _build_robtarget(target)


def _parse_speed(speed) -> str | list[float]:
    """Convert speed to generator-compatible form (string or [v_tcp])."""
    if isinstance(speed, str):
        return speed
    if isinstance(speed, list) and speed:
        return [float(speed[0])]
    if isinstance(speed, dict):
        return [float(speed.get("v_tcp", 200))]
    return [200.0]


def _build_move_command(cmd_dict: dict, index: int) -> MoveCommand:
    """
    Convert one MoveCommand dict to the internal MoveCommand dataclass.

    Handles both:
    - parse.py format: command_type, target (nested dataclass dict), speed (str/list)
    - OpenAPI format:  type, target (trans/rot arrays), speed (SpeedData dict)
    """
    # Support both 'command_type' (parse.py) and 'type' (OpenAPI)
    cmd_type = cmd_dict.get("command_type") or cmd_dict.get("type", "MoveJ")
    target_raw = cmd_dict.get("target", {})
    # String targets are variable references resolved by TrajectoryGenerator's var_table
    target = target_raw if isinstance(target_raw, str) else _build_target(target_raw)

    speed = _parse_speed(cmd_dict.get("speed", [200.0]))
    zone = cmd_dict.get("zone", "z0")

    # MoveC: circular_point (parse.py) or via_point (OpenAPI)
    cir_point = None
    via = cmd_dict.get("circular_point") or cmd_dict.get("via_point")
    if via and not isinstance(via, str):
        cir_point = _build_robtarget(via)

    return MoveCommand(
        command_type=cmd_type,
        target=target,
        speed=speed,
        zone=zone,
        tool=cmd_dict.get("tool", "tool0"),
        circular_point=cir_point,
        line_number=index,
    )


def _build_tooldata(td: dict) -> ToolData:
    """Convert a tooldata dict to ToolData dataclass."""
    tcp = td.get("tcp_pos", {})
    rot = td.get("tcp_rot", {})
    return ToolData(
        tcp_pos=Position(x=tcp.get("x", 0), y=tcp.get("y", 0), z=tcp.get("z", 0)),
        tcp_rot=Orientation(q1=rot.get("q1", 1), q2=rot.get("q2", 0), q3=rot.get("q3", 0), q4=rot.get("q4", 0)),
        robhold=td.get("robhold", True),
    )


def _build_declaration(decl_dict: dict) -> Declaration | None:
    """Convert a declaration dict from parse.py _to_dict output to a Declaration dataclass."""
    value_raw = decl_dict.get("value")
    if isinstance(value_raw, dict):
        if "tcp_pos" in value_raw:
            value = _build_tooldata(value_raw)
        elif "position" in value_raw or "trans" in value_raw:
            value = _build_robtarget(value_raw)
        elif "robot_axes" in value_raw:
            value = _build_jointtarget(value_raw)
        else:
            return None
    else:
        return None  # skip non-target declarations (strings, floats, etc.)
    return Declaration(
        dtype=decl_dict.get("dtype", "CONST"),
        type_name=decl_dict.get("type_name", "robtarget"),
        name=decl_dict["name"],
        value=value,
    )


def _build_program_from_dict(prog_dict: dict) -> Program:
    """
    Reconstruct a full Program from parse.py's _to_dict output.
    Preserves declarations so variable references (e.g. 'p10') can be resolved.
    """
    modules = []
    for mod_dict in prog_dict.get("modules", []):
        declarations = []
        for d in mod_dict.get("declarations", []):
            decl = _build_declaration(d)
            if decl:
                declarations.append(decl)

        procedures = []
        for proc_dict in mod_dict.get("procedures", []):
            cmds = [_build_move_command(c, i) for i, c in enumerate(proc_dict.get("commands", []))]
            procedures.append(Procedure(name=proc_dict.get("name", "main"), commands=cmds))

        modules.append(Module(
            name=mod_dict.get("name", "MainModule"),
            procedures=procedures,
            declarations=declarations,
        ))
    return Program(modules=modules)


def _build_program(commands: list[dict]) -> Program:
    """Wrap a flat list of MoveCommand dicts into a minimal Program (no declarations)."""
    move_cmds = [_build_move_command(c, i) for i, c in enumerate(commands)]
    procedure = Procedure(name="main", commands=move_cmds)
    module = Module(name="MainModule", procedures=[procedure], declarations=[])
    return Program(modules=[module])


# ---------------------------------------------------------------------------
# Sync helper (runs in thread pool)
# ---------------------------------------------------------------------------

MM_PER_M = 1000.0


def _run_simulation_sync(request: SimulateRequest, start_ms: float) -> SimulateResponse:
    """
    CPU-bound simulation work — executed in a thread pool via run_in_executor.

    Raises HTTPException for known error cases so the executor propagates it.
    """
    simulate_timeout_s = 10.0
    deadline = time.monotonic() + simulate_timeout_s

    try:
        if request.program:
            program = _build_program_from_dict(request.program)
        else:
            program = _build_program(request.ast)
        raw_waypoints, timed_out = _generator.generate(program, request.robot_id, deadline=deadline)
    except TrajectoryError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.exception("Unexpected error during simulation")
        raise HTTPException(status_code=500, detail=f"Simulation failed: {e}")

    # ----- Collision detection (skip if no obstacles) -----
    collision_map: dict[int, list[dict]] = {}  # waypoint_index → collisions
    loaded_obstacle_ids: list[str] = []

    if request.obstacles:
        try:
            for obs in request.obstacles:
                stl_path = f"/tmp/obstacles/{obs.obstacle_id}.stl"
                _detector.load_obstacle(obs.obstacle_id, stl_path, obs.position, obs.rotation)
                loaded_obstacle_ids.append(obs.obstacle_id)

            joint_trajectory = [wp["joints"] for wp in raw_waypoints]
            collision_results = _detector.check_trajectory_collisions(
                request.robot_id, joint_trajectory
            )
            for result in collision_results:
                collision_map[result["waypoint_index"]] = result["collisions"]
        except FileNotFoundError as e:
            logger.warning(f"Obstacle file not found, skipping collision check: {e}")
        except Exception as e:
            logger.warning(f"Collision detection failed, skipping: {e}")
        finally:
            for obs_id in loaded_obstacle_ids:
                _detector.remove_obstacle(obs_id)

    # ----- Build response waypoints -----
    total_collisions = 0
    waypoints: list[TrajectoryWaypoint] = []
    for i, wp in enumerate(raw_waypoints):
        joints_deg = [math.degrees(j) for j in wp["joints"]]
        pos_mm = [c * MM_PER_M for c in wp["position"]]

        wp_collisions = []
        if i in collision_map:
            for c in collision_map[i]:
                wp_collisions.append(CollisionInfo(
                    obstacle_id=c["obstacle_id"],
                    link=f"Link{c['link_index']}",
                    penetration_depth=c["penetration_depth"],
                    contact_point=c["contact_point"],
                ))
            total_collisions += len(wp_collisions)

        waypoints.append(TrajectoryWaypoint(
            index=i,
            timestamp=wp["timestamp"],
            joints=joints_deg,
            tcp_pose=TCPPose(position=pos_mm, orientation=[1.0, 0.0, 0.0, 0.0]),
            collisions=wp_collisions,
        ))

    duration = raw_waypoints[-1]["timestamp"] if raw_waypoints else 0.0
    elapsed_ms = time.monotonic() * 1000 - start_ms

    stats = SimulationStats(
        total_waypoints=len(waypoints),
        duration_seconds=round(duration, 3),
        collisions_detected=total_collisions,
        ik_failures=0,
        computation_time_ms=round(elapsed_ms, 1),
        timed_out=timed_out,
    )

    return SimulateResponse(trajectory=waypoints, stats=stats)


# ---------------------------------------------------------------------------
# Endpoint
# ---------------------------------------------------------------------------

@router.post("/api/simulate", response_model=SimulateResponse)
async def simulate(request: SimulateRequest):
    """
    Full pipeline: MoveCommand[] → IK → trajectory waypoints.

    1. Reconstruct Program AST from flat MoveCommand list
    2. Run TrajectoryGenerator to get joint-angle waypoints (radians)
    3. Convert to TrajectoryWaypoint response (joints in degrees)
    """
    start_ms = time.monotonic() * 1000

    if request.robot_id not in ("irb4600", "irb2600", "irb6700"):
        raise HTTPException(status_code=400, detail=f"Unknown robot_id: {request.robot_id!r}")

    if not request.program and not request.ast:
        raise HTTPException(status_code=400, detail="Provide either 'program' or 'ast'")

    loop = asyncio.get_event_loop()
    async with pybullet_lock:
        try:
            result = await loop.run_in_executor(
                executor, functools.partial(_run_simulation_sync, request, start_ms)
            )
        except HTTPException:
            raise
        except Exception as e:
            logger.exception("Unexpected error during simulation")
            raise HTTPException(status_code=500, detail=f"Simulation failed: {e}")
    return result
