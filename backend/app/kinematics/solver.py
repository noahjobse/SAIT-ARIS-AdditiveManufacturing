"""Forward and inverse kinematics solver using PyBullet."""
import logging
from typing import List, Optional, Dict

import numpy as np
import pybullet as p

from .robot_loader import RobotLoader
from .exceptions import InvalidJointAnglesError, IKSolutionNotFoundError

logger = logging.getLogger(__name__)


class KinematicsSolver:
    """Kinematics solver for robot forward and inverse kinematics."""

    def __init__(self, headless: bool = True):
        """
        Initialize solver with PyBullet robot loader.

        Args:
            headless: If True, run PyBullet without GUI
        """
        self.loader = RobotLoader(headless=headless)

    def disconnect(self):
        """Disconnect from PyBullet."""
        self.loader.disconnect()

    def forward_kinematics(
        self, robot_id: str, joint_angles: List[float]
    ) -> Dict[str, List[float]]:
        """
        Calculate end-effector pose from joint angles.

        Args:
            robot_id: Robot identifier (e.g., 'irb4600')
            joint_angles: List of joint angles in radians [j1, j2, j3, j4, j5, j6]

        Returns:
            Dict with 'position' [x, y, z] and 'orientation' [qx, qy, qz, qw]

        Raises:
            ValueError: If joint_angles length doesn't match robot DOF
            InvalidJointAnglesError: If joint angles violate limits
        """
        # Load robot if not already loaded
        if not self.loader.is_loaded(robot_id):
            self.loader.load_robot(robot_id)

        pybullet_id = self.loader.get_pybullet_id(robot_id)
        num_joints = self.loader.get_joint_count(robot_id)

        # Validate input
        if len(joint_angles) != num_joints:
            raise ValueError(f"Expected {num_joints} joint angles, got {len(joint_angles)}")

        # Validate joint limits
        self._validate_joint_limits(robot_id, joint_angles)

        # Set joint positions in PyBullet
        for joint_idx in range(num_joints):
            p.resetJointState(
                pybullet_id,
                joint_idx,
                joint_angles[joint_idx],
                physicsClientId=self.loader.physics_client,
            )

        # Get end-effector link state (link_6 or tool0)
        # Link index for tool0 is num_joints (last link)
        link_state = p.getLinkState(
            pybullet_id,
            num_joints,  # tool0 link index
            physicsClientId=self.loader.physics_client,
        )

        position = list(link_state[4])  # World position
        orientation = list(link_state[5])  # World orientation (quaternion)

        logger.debug(f"FK result for {robot_id}: pos={position}, ori={orientation}")

        return {
            "position": position,
            "orientation": orientation,
        }

    def _validate_joint_limits(self, robot_id: str, joint_angles: List[float]):
        """
        Validate joint angles against joint limits.

        Raises:
            InvalidJointAnglesError: If any joint exceeds limits
        """
        limits = self.loader.get_joint_limits(robot_id)

        for joint_idx, angle in enumerate(joint_angles):
            lower = limits[joint_idx]["lower"]
            upper = limits[joint_idx]["upper"]

            if angle < lower or angle > upper:
                raise InvalidJointAnglesError(
                    robot_id, joint_idx, angle, (lower, upper)
                )
