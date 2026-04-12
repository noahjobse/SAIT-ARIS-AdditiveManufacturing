"""
Trajectory generator: converts a parsed RAPID Program into a list of
time-stamped joint-angle waypoints via PyBullet IK.
"""
import logging
import math
import time

import numpy as np

from app.kinematics.solver import KinematicsSolver
from app.parser.ast_nodes import JointTarget, MoveCommand, Program, RobTarget, ToolData

logger = logging.getLogger(__name__)

# Fixed controller timestep (matches real ABB controller cycle time)
DT = 0.02  # seconds

# Named RAPID speed zones → TCP speed in mm/s
RAPID_SPEEDS = {
    "v5": 5, "v10": 10, "v20": 20, "v30": 30, "v40": 40, "v50": 50,
    "v60": 60, "v80": 80, "v100": 100, "v150": 150, "v200": 200,
    "v300": 300, "v400": 400, "v500": 500, "v600": 600, "v800": 800,
    "v1000": 1000, "v1500": 1500, "v2000": 2000, "v2500": 2500,
    "v3000": 3000, "v4000": 4000, "v5000": 5000,
    "vmax": 5000,
}

MM_TO_M = 0.001


class TrajectoryError(Exception):
    """Raised when trajectory generation fails (bad target, IK failure, etc.)."""


class TrajectoryGenerator:
    """
    Converts a parsed RAPID Program into a list of waypoints.

    Each waypoint:
        {
            "joints":    [j1, j2, j3, j4, j5, j6],  # radians
            "timestamp": float,                       # seconds from start
            "position":  [x, y, z],                  # meters
        }
    """

    def __init__(self, solver: KinematicsSolver):
        self.solver = solver

    def generate(self, program: Program, robot_id: str, deadline: float | None = None) -> list[dict]:
        """
        Generate waypoints for the first procedure in the program.

        Args:
            program: Parsed RAPID program
            robot_id: Robot identifier (e.g. 'irb4600')
            deadline: Monotonic clock deadline (seconds). If exceeded, returns
                      partial results with whatever waypoints were generated.

        Returns:
            List of waypoint dicts

        Raises:
            TrajectoryError: If a target cannot be resolved or IK fails
        """
        if not program.modules:
            raise TrajectoryError("Program has no modules")

        module = program.modules[0]

        # Build variable lookup: name -> RobTarget, JointTarget, or ToolData
        var_table: dict[str, RobTarget | JointTarget | ToolData] = {}
        for decl in module.declarations:
            if isinstance(decl.value, (RobTarget, JointTarget, ToolData)):
                var_table[decl.name] = decl.value

        if not module.procedures:
            raise TrajectoryError("Module has no procedures")

        procedure = module.procedures[0]
        waypoints: list[dict] = []
        current_time = 0.0
        current_joints: list[float] | None = None

        timed_out = False
        for i, cmd in enumerate(procedure.commands):
            if deadline is not None and time.monotonic() > deadline:
                logger.warning("Trajectory generation timed out after %d waypoints", len(waypoints))
                timed_out = True
                break

            new_waypoints, current_joints = self._process_command(
                cmd, var_table, robot_id, current_joints, current_time
            )
            for wp in new_waypoints:
                wp["command_index"] = i
            if new_waypoints:
                current_time = new_waypoints[-1]["timestamp"]
            waypoints.extend(new_waypoints)

        return waypoints, timed_out

    # ------------------------------------------------------------------
    # Command dispatch
    # ------------------------------------------------------------------

    def _process_command(
        self,
        cmd: MoveCommand,
        var_table: dict,
        robot_id: str,
        current_joints: list[float] | None,
        start_time: float,
    ) -> tuple[list[dict], list[float] | None]:
        """Route a MoveCommand to the correct interpolation method."""
        if cmd.command_type == "MoveL":
            return self._move_l(cmd, var_table, robot_id, current_joints, start_time)
        if cmd.command_type == "MoveJ":
            return self._move_j(cmd, var_table, robot_id, current_joints, start_time)
        if cmd.command_type == "MoveAbsJ":
            return self._move_abs_j(cmd, var_table, robot_id, current_joints, start_time)
        if cmd.command_type == "MoveC":
            return self._move_c(cmd, var_table, robot_id, current_joints, start_time)

        logger.warning("Unknown command type '%s', skipping", cmd.command_type)
        return [], current_joints

    # ------------------------------------------------------------------
    # MoveL — linear Cartesian interpolation
    # ------------------------------------------------------------------

    def _move_l(self, cmd, var_table, robot_id, current_joints, start_time):
        target = self._resolve_target(cmd.target, var_table, cmd.command_type)
        if not isinstance(target, RobTarget):
            raise TrajectoryError(f"MoveL requires a robtarget, got {type(target).__name__}")

        speed_mms = self._parse_speed(cmd.speed)
        end_pos_m = self._pos_to_meters(target.position)
        orientation = [target.orientation.q2, target.orientation.q3, target.orientation.q4, target.orientation.q1]  # RAPID [w,x,y,z] → PyBullet [x,y,z,w]

        # Apply tool TCP offset — IK solves for flange, not tool tip
        tool = self._resolve_tool(cmd.tool, var_table)
        if tool:
            end_pos_m = self._apply_tool_offset(end_pos_m, orientation, tool)

        # Determine start position (use FK if we have joints, else start at target)
        if current_joints is not None:
            fk = self.solver.forward_kinematics(robot_id, current_joints)
            start_pos_m = fk["position"]
        else:
            start_pos_m = end_pos_m

        dist_m = np.linalg.norm(np.array(end_pos_m) - np.array(start_pos_m))
        n_steps = max(1, math.ceil(dist_m / (speed_mms * MM_TO_M * DT)))

        waypoints = []
        t = start_time
        for i in range(1, n_steps + 1):
            alpha = i / n_steps
            pos = (np.array(start_pos_m) + alpha * (np.array(end_pos_m) - np.array(start_pos_m))).tolist()
            t += DT
            ik = self.solver.inverse_kinematics(robot_id, pos, orientation, current_joints)
            current_joints = ik["joint_angles"]
            waypoints.append({"joints": current_joints, "timestamp": round(t, 4), "position": pos})

        return waypoints, current_joints

    # ------------------------------------------------------------------
    # MoveJ — joint-space interpolation
    # ------------------------------------------------------------------

    def _move_j(self, cmd, var_table, robot_id, current_joints, start_time):
        target = self._resolve_target(cmd.target, var_table, cmd.command_type)
        if not isinstance(target, RobTarget):
            raise TrajectoryError(f"MoveJ requires a robtarget, got {type(target).__name__}")

        speed_mms = self._parse_speed(cmd.speed)
        end_pos_m = self._pos_to_meters(target.position)
        orientation = [target.orientation.q2, target.orientation.q3, target.orientation.q4, target.orientation.q1]  # RAPID [w,x,y,z] → PyBullet [x,y,z,w]

        # Apply tool TCP offset
        tool = self._resolve_tool(cmd.tool, var_table)
        if tool:
            end_pos_m = self._apply_tool_offset(end_pos_m, orientation, tool)

        # Solve IK at the target to get end joint angles
        end_joints = self.solver.inverse_kinematics(robot_id, end_pos_m, orientation, current_joints)["joint_angles"]

        if current_joints is None:
            current_joints = [0.0] * len(end_joints)

        # Estimate duration from Cartesian distance (approximation for joint moves)
        fk = self.solver.forward_kinematics(robot_id, current_joints)
        dist_m = np.linalg.norm(np.array(end_pos_m) - np.array(fk["position"]))
        n_steps = max(1, math.ceil(dist_m / (speed_mms * MM_TO_M * DT)))

        waypoints = []
        t = start_time
        start_j = list(current_joints)
        for i in range(1, n_steps + 1):
            alpha = i / n_steps
            joints = [s + alpha * (e - s) for s, e in zip(start_j, end_joints)]
            t += DT
            fk_step = self.solver.forward_kinematics(robot_id, joints)
            waypoints.append({"joints": joints, "timestamp": round(t, 4), "position": fk_step["position"]})

        return waypoints, end_joints

    # ------------------------------------------------------------------
    # MoveAbsJ — direct joint target (no IK needed)
    # ------------------------------------------------------------------

    def _move_abs_j(self, cmd, var_table, robot_id, current_joints, start_time):
        target = self._resolve_target(cmd.target, var_table, cmd.command_type)
        if not isinstance(target, JointTarget):
            raise TrajectoryError(f"MoveAbsJ requires a jointtarget, got {type(target).__name__}")

        speed_mms = self._parse_speed(cmd.speed)
        end_joints = target.robot_axes  # Already joint angles in degrees — convert to radians
        end_joints_rad = [math.radians(j) for j in end_joints]

        if current_joints is None:
            current_joints = [0.0] * len(end_joints_rad)

        joint_range = max(abs(e - s) for s, e in zip(current_joints, end_joints_rad))
        n_steps = max(1, math.ceil(joint_range / (math.radians(speed_mms / 100) * DT)))

        waypoints = []
        t = start_time
        start_j = list(current_joints)
        for i in range(1, n_steps + 1):
            alpha = i / n_steps
            joints = [s + alpha * (e - s) for s, e in zip(start_j, end_joints_rad)]
            t += DT
            fk = self.solver.forward_kinematics(robot_id, joints)
            waypoints.append({"joints": joints, "timestamp": round(t, 4), "position": fk["position"]})

        return waypoints, end_joints_rad

    # ------------------------------------------------------------------
    # MoveC — circular arc interpolation
    # ------------------------------------------------------------------

    def _move_c(self, cmd, var_table, robot_id, current_joints, start_time):
        target = self._resolve_target(cmd.target, var_table, cmd.command_type)
        cir = self._resolve_target(cmd.circular_point, var_table, "MoveC.cir_point")

        if not isinstance(target, RobTarget) or not isinstance(cir, RobTarget):
            raise TrajectoryError("MoveC requires robtargets for both target and cir_point")

        speed_mms = self._parse_speed(cmd.speed)
        orientation = [target.orientation.q2, target.orientation.q3, target.orientation.q4, target.orientation.q1]  # RAPID [w,x,y,z] → PyBullet [x,y,z,w]

        # Three points defining the arc: start (current EE) → via → end
        if current_joints is not None:
            fk = self.solver.forward_kinematics(robot_id, current_joints)
            p_start = np.array(fk["position"])
        else:
            p_start = np.array(self._pos_to_meters(cir.position))  # fallback

        p_via = np.array(self._pos_to_meters(cir.position))
        p_end = np.array(self._pos_to_meters(target.position))

        # Apply tool TCP offset to all arc points
        tool = self._resolve_tool(cmd.tool, var_table)
        if tool:
            p_via = np.array(self._apply_tool_offset(p_via.tolist(), orientation, tool))
            p_end = np.array(self._apply_tool_offset(p_end.tolist(), orientation, tool))

        arc_points = self._arc_interpolate(p_start, p_via, p_end, speed_mms)

        waypoints = []
        t = start_time
        for pos in arc_points:
            t += DT
            ik = self.solver.inverse_kinematics(robot_id, pos.tolist(), orientation, current_joints)
            current_joints = ik["joint_angles"]
            waypoints.append({"joints": current_joints, "timestamp": round(t, 4), "position": pos.tolist()})

        return waypoints, current_joints

    def _arc_interpolate(self, p1: np.ndarray, p2: np.ndarray, p3: np.ndarray, speed_mms: float) -> list[np.ndarray]:
        """
        Fit a circle through three 3D points and return evenly spaced arc points.
        Falls back to linear interpolation if the three points are collinear.
        """
        # Vectors in the plane of the three points
        v1 = p2 - p1
        v2 = p3 - p1
        normal = np.cross(v1, v2)
        norm_len = np.linalg.norm(normal)

        if norm_len < 1e-9:
            # Collinear — degenerate arc, fall back to straight line
            dist_m = np.linalg.norm(p3 - p1)
            n_steps = max(1, math.ceil(dist_m / (speed_mms * MM_TO_M * DT)))
            return [p1 + (i / n_steps) * (p3 - p1) for i in range(1, n_steps + 1)]

        normal = normal / norm_len

        # Find circumcenter of the triangle p1, p2, p3
        ax = np.dot(v1, v1)
        bx = np.dot(v1, v2)
        by = np.dot(v2, v2)
        cx, cy = ax / 2, bx / 2  # RHS for the circumcenter system
        denom = ax * by - bx * bx
        if abs(denom) < 1e-12:
            # Near-degenerate, fall back
            dist_m = np.linalg.norm(p3 - p1)
            n_steps = max(1, math.ceil(dist_m / (speed_mms * MM_TO_M * DT)))
            return [p1 + (i / n_steps) * (p3 - p1) for i in range(1, n_steps + 1)]

        s = (cx * by - cy * bx) / denom
        t_val = (ax * cy - bx * cx) / denom
        center = p1 + s * v1 + t_val * v2
        radius = np.linalg.norm(p1 - center)

        # Parameterize arc from p1 to p3 through p2
        def angle_from_center(pt):
            vec = pt - center
            vec_proj = vec - np.dot(vec, normal) * normal
            return vec_proj

        r1 = angle_from_center(p1)
        r2 = angle_from_center(p2)
        r3 = angle_from_center(p3)

        r1n = r1 / (np.linalg.norm(r1) + 1e-12)
        r3n = r3 / (np.linalg.norm(r3) + 1e-12)
        total_angle = math.acos(np.clip(np.dot(r1n, r3n), -1, 1))

        # Determine sweep direction via the via point
        cross = np.cross(r1, r2)
        if np.dot(cross, normal) < 0:
            total_angle = 2 * math.pi - total_angle

        arc_len_m = radius * total_angle
        n_steps = max(1, math.ceil(arc_len_m / (speed_mms * MM_TO_M * DT)))

        points = []
        for i in range(1, n_steps + 1):
            theta = (i / n_steps) * total_angle
            # Rodrigues' rotation formula: rotate r1 around normal by theta
            r1_rot = (r1 * math.cos(theta)
                      + np.cross(normal, r1) * math.sin(theta)
                      + normal * np.dot(normal, r1) * (1 - math.cos(theta)))
            points.append(center + r1_rot)

        return points

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _resolve_target(self, target, var_table: dict, context: str):
        """Resolve a target: if it's a string variable name, look it up."""
        if isinstance(target, str):
            if target not in var_table:
                raise TrajectoryError(
                    f"{context}: unresolved target variable '{target}'. "
                    f"Declared variables: {list(var_table.keys())}"
                )
            return var_table[target]
        return target

    def _parse_speed(self, speed) -> float:
        """Parse RAPID speed to mm/s. Accepts named zones or speeddata lists."""
        if isinstance(speed, str):
            key = speed.lower()
            if key in RAPID_SPEEDS:
                return float(RAPID_SPEEDS[key])
            raise TrajectoryError(f"Unknown RAPID speed zone: '{speed}'")
        if isinstance(speed, list) and speed:
            return float(speed[0])  # v_tcp is the first element
        raise TrajectoryError(f"Cannot parse speed: {speed!r}")

    def _pos_to_meters(self, pos) -> list[float]:
        """Convert RAPID position (mm) to meters."""
        return [pos.x * MM_TO_M, pos.y * MM_TO_M, pos.z * MM_TO_M]

    def _resolve_tool(self, tool_name: str, var_table: dict) -> ToolData | None:
        """Look up a tool by name. Returns None for tool0 (no offset)."""
        if tool_name == "tool0":
            return None
        tool = var_table.get(tool_name)
        if isinstance(tool, ToolData):
            return tool
        return None

    def _apply_tool_offset(
        self, target_pos_m: list[float], target_ori_xyzw: list[float], tool: ToolData
    ) -> list[float]:
        """
        Compute flange position from TCP target and tool offset.

        The tool TCP offset is defined in the tool frame (rotates with end-effector).
        flange_pos = target_pos - R(target_orientation) * tool_offset

        Args:
            target_pos_m: Desired TCP position in meters [x, y, z]
            target_ori_xyzw: Target orientation as [qx, qy, qz, qw]
            tool: ToolData with TCP offset in mm

        Returns:
            Flange position in meters [x, y, z]
        """
        # Tool offset in meters
        tool_offset_m = np.array([
            tool.tcp_pos.x * MM_TO_M,
            tool.tcp_pos.y * MM_TO_M,
            tool.tcp_pos.z * MM_TO_M,
        ])

        if np.linalg.norm(tool_offset_m) < 1e-9:
            return target_pos_m

        # Rotate tool offset by target orientation using quaternion rotation
        # q * v * q_conjugate
        qx, qy, qz, qw = target_ori_xyzw
        q = np.array([qw, qx, qy, qz])  # scipy convention [w, x, y, z]

        # Quaternion rotation: v' = q * v * q*
        # Using Rodrigues-like formula for efficiency
        u = q[1:4]  # vector part
        s = q[0]     # scalar part
        rotated = 2.0 * np.dot(u, tool_offset_m) * u \
                  + (s * s - np.dot(u, u)) * tool_offset_m \
                  + 2.0 * s * np.cross(u, tool_offset_m)

        # Flange = TCP target - rotated tool offset
        flange_pos = np.array(target_pos_m) - rotated
        return flange_pos.tolist()
