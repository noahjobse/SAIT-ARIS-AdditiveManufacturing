"""
POST /api/simulate — full pipeline: MoveCommand[] → trajectory waypoints.

Bridges the frontend's flat MoveCommand list to the internal Program AST,
runs TrajectoryGenerator (IK-backed), and returns timestamped waypoints.
"""
import logging
import math
import time

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

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
)
from app.schemas.simulate import (
    CollisionInfo,
    SimulateResponse,
    SimulationStats,
    TCPPose,
    TrajectoryWaypoint,
)
from app.trajectory.generator import TrajectoryError, TrajectoryGenerator

router = APIRouter()
logger = logging.getLogger(__name__)

# Shared solver (PyBullet headless) — created once at import time
_solver = KinematicsSolver()
_generator = TrajectoryGenerator(_solver)

# ---------------------------------------------------------------------------
# Request schema
# ---------------------------------------------------------------------------

class ObstacleTransform(BaseModel):
    obstacle_id: str
    position: list[float] = [0.0, 0.0, 0.0]
    rotation: list[float] = [0.0, 0.0, 0.0]


class SimulateRequest(BaseModel):
    robot_id: str
    ast: list[dict]          # MoveCommand dicts from the frontend
    obstacles: list[ObstacleTransform] = []


# ---------------------------------------------------------------------------
# Bridge: frontend MoveCommand dict → Python dataclass
# ---------------------------------------------------------------------------

def _build_robtarget(target: dict) -> RobTarget:
    """
    Convert a RobTarget dict to the Python dataclass.

    Handles two formats:
    - parse.py output: { pos: {x,y,z}, rot: {q1,q2,q3,q4} }
    - OpenAPI schema:  { type: "RobTarget", trans: [x,y,z], rot: [q1,q2,q3,q4] }
    """
    if "pos" in target:
        # Python dataclass dict (from parse.py _to_dict)
        p = target["pos"]
        r = target["rot"]
        return RobTarget(
            pos=Position(x=p["x"], y=p["y"], z=p["z"]),
            rot=Orientation(q1=r["q1"], q2=r["q2"], q3=r["q3"], q4=r["q4"]),
        )
    # OpenAPI schema format (trans array, rot array)
    trans = target.get("trans", [0.0, 0.0, 0.0])
    rot = target.get("rot", [1.0, 0.0, 0.0, 0.0])
    return RobTarget(
        pos=Position(x=trans[0], y=trans[1], z=trans[2]),
        rot=Orientation(q1=rot[0], q2=rot[1], q3=rot[2], q4=rot[3]),
    )


def _build_jointtarget(target: dict) -> JointTarget:
    return JointTarget(
        robax=target.get("robax", [0.0] * 6),
        extax=target.get("extax", [0.0] * 6),
    )


def _build_target(target: dict) -> RobTarget | JointTarget:
    """Detect and convert a target dict, supporting both dict formats."""
    # Python dataclass dict has 'robax' key for JointTarget
    if "robax" in target:
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
    target_dict = cmd_dict.get("target", {})
    target = _build_target(target_dict)

    speed = _parse_speed(cmd_dict.get("speed", [200.0]))
    zone = cmd_dict.get("zone", "z0")

    # MoveC: cir_point (parse.py) or via_point (OpenAPI)
    cir_point = None
    via = cmd_dict.get("cir_point") or cmd_dict.get("via_point")
    if via:
        cir_point = _build_robtarget(via)

    return MoveCommand(
        command_type=cmd_type,
        target=target,
        speed=speed,
        zone=zone,
        tool=cmd_dict.get("tool", "tool0"),
        cir_point=cir_point,
        line_number=index,
    )


def _build_program(commands: list[dict]) -> Program:
    """Wrap a flat list of frontend MoveCommands into a minimal Program AST."""
    move_cmds = [_build_move_command(c, i) for i, c in enumerate(commands)]
    procedure = Procedure(name="main", commands=move_cmds)
    module = Module(name="MainModule", procedures=[procedure], declarations=[])
    return Program(modules=[module])


# ---------------------------------------------------------------------------
# Endpoint
# ---------------------------------------------------------------------------

MM_PER_M = 1000.0


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

    if not request.ast:
        raise HTTPException(status_code=400, detail="ast must contain at least one MoveCommand")

    try:
        program = _build_program(request.ast)
        raw_waypoints = _generator.generate(program, request.robot_id)
    except TrajectoryError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.exception("Unexpected error during simulation")
        raise HTTPException(status_code=500, detail=f"Simulation failed: {e}")

    # Build response waypoints — convert joints rad→deg, position m→mm
    waypoints: list[TrajectoryWaypoint] = []
    for i, wp in enumerate(raw_waypoints):
        joints_deg = [math.degrees(j) for j in wp["joints"]]
        pos_mm = [c * MM_PER_M for c in wp["position"]]
        waypoints.append(TrajectoryWaypoint(
            index=i,
            timestamp=wp["timestamp"],
            joints=joints_deg,
            tcp_pose=TCPPose(position=pos_mm, orientation=[1.0, 0.0, 0.0, 0.0]),
            collisions=[],
        ))

    duration = raw_waypoints[-1]["timestamp"] if raw_waypoints else 0.0
    elapsed_ms = time.monotonic() * 1000 - start_ms

    stats = SimulationStats(
        total_waypoints=len(waypoints),
        duration_seconds=round(duration, 3),
        collisions_detected=0,
        ik_failures=0,
        computation_time_ms=round(elapsed_ms, 1),
    )

    return SimulateResponse(trajectory=waypoints, stats=stats)
