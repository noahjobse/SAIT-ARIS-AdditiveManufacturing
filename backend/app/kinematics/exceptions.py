"""Custom exceptions for kinematics operations."""


class KinematicsError(Exception):
    """Base exception for kinematics module."""

    pass


class RobotNotLoadedError(KinematicsError):
    """Raised when attempting to use a robot that hasn't been loaded."""

    def __init__(self, robot_id: str):
        self.robot_id = robot_id
        super().__init__(f"Robot '{robot_id}' not loaded in PyBullet")


class IKSolutionNotFoundError(KinematicsError):
    """Raised when inverse kinematics cannot find a solution."""

    def __init__(self, robot_id: str, target_position: list):
        self.robot_id = robot_id
        self.target_position = target_position
        super().__init__(
            f"IK solution not found for robot '{robot_id}' at target {target_position}"
        )


class InvalidJointAnglesError(KinematicsError):
    """Raised when joint angles violate joint limits."""

    def __init__(self, robot_id: str, joint_index: int, value: float, limit_range: tuple):
        self.robot_id = robot_id
        self.joint_index = joint_index
        self.value = value
        self.limit_range = limit_range
        super().__init__(
            f"Joint {joint_index} value {value:.3f} outside limits {limit_range} for robot '{robot_id}'"
        )
