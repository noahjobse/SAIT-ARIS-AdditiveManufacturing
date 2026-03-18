"""
Pydantic models for POST /api/simulate request and response.
"""
from pydantic import BaseModel


class TCPPose(BaseModel):
    position: list[float]   # [x, y, z] in millimeters
    orientation: list[float]  # [q1, q2, q3, q4]


class CollisionInfo(BaseModel):
    obstacle_id: str
    link: str
    penetration_depth: float
    contact_point: list[float]


class TrajectoryWaypoint(BaseModel):
    index: int
    timestamp: float
    joints: list[float]      # degrees (j1-j6)
    tcp_pose: TCPPose
    collisions: list[CollisionInfo]


class SimulationStats(BaseModel):
    total_waypoints: int
    duration_seconds: float
    collisions_detected: int
    ik_failures: int
    computation_time_ms: float
    timed_out: bool = False


class SimulateResponse(BaseModel):
    trajectory: list[TrajectoryWaypoint]
    stats: SimulationStats
