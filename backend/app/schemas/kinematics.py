"""Pydantic schemas for kinematics API endpoints."""

from pydantic import BaseModel, Field


class FKRequest(BaseModel):
    """Request for forward kinematics calculation."""

    robot_id: str = Field(..., description="Robot identifier (e.g., 'irb4600')")
    joint_angles: list[float] = Field(
        ..., description="Joint angles in radians [j1, j2, j3, j4, j5, j6]"
    )


class FKResponse(BaseModel):
    """Response for forward kinematics calculation."""

    robot_id: str
    position: list[float] = Field(..., description="End-effector position [x, y, z] in meters")
    orientation: list[float] = Field(
        ..., description="End-effector orientation quaternion [qx, qy, qz, qw]"
    )


class IKRequest(BaseModel):
    """Request for inverse kinematics calculation."""

    robot_id: str = Field(..., description="Robot identifier (e.g., 'irb4600')")
    target_position: list[float] = Field(
        ..., description="Target position [x, y, z] in meters"
    )
    target_orientation: list[float] | None = Field(
        None, description="Target orientation quaternion [qx, qy, qz, qw] (optional)"
    )
    current_joints: list[float] | None = Field(
        None, description="Current joint angles as IK seed (optional)"
    )


class IKResponse(BaseModel):
    """Response for inverse kinematics calculation."""

    robot_id: str
    joint_angles: list[float] = Field(
        ..., description="Calculated joint angles in radians [j1, j2, j3, j4, j5, j6]"
    )
