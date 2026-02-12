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

    def inverse_kinematics(
        self,
        robot_id: str,
        target_position: List[float],
        target_orientation: Optional[List[float]] = None,
        current_joints: Optional[List[float]] = None,
    ) -> Dict[str, List[float]]:
        """
        Calculate joint angles to reach target end-effector pose.

        Args:
            robot_id: Robot identifier (e.g., 'irb4600')
            target_position: Target position [x, y, z] in meters
            target_orientation: Target orientation [qx, qy, qz, qw] (optional)
            current_joints: Current joint angles as IK seed (optional)

        Returns:
            Dict with 'joint_angles' list

        Raises:
            IKSolutionNotFoundError: If IK cannot find a solution
        """
        # Load robot if not already loaded
        if not self.loader.is_loaded(robot_id):
            self.loader.load_robot(robot_id)

        pybullet_id = self.loader.get_pybullet_id(robot_id)
        num_joints = self.loader.get_joint_count(robot_id)

        # Set current joints as starting position (if provided)
        if current_joints is not None:
            if len(current_joints) != num_joints:
                raise ValueError(
                    f"Expected {num_joints} current joints, got {len(current_joints)}"
                )
            for joint_idx in range(num_joints):
                p.resetJointState(
                    pybullet_id,
                    joint_idx,
                    current_joints[joint_idx],
                    physicsClientId=self.loader.physics_client,
                )

        # Use default orientation if not provided
        if target_orientation is None:
            target_orientation = [0, 0, 0, 1]  # Identity quaternion

        # Get joint limits for PyBullet IK
        limits = self.loader.get_joint_limits(robot_id)
        lower_limits = [lim["lower"] for lim in limits]
        upper_limits = [lim["upper"] for lim in limits]
        joint_ranges = [upper - lower for upper, lower in zip(upper_limits, lower_limits)]
        rest_poses = [(upper + lower) / 2 for upper, lower in zip(upper_limits, lower_limits)]

        # Call PyBullet IK solver
        joint_angles = p.calculateInverseKinematics(
            pybullet_id,
            num_joints,  # End-effector link index (tool0)
            target_position,
            targetOrientation=target_orientation,
            lowerLimits=lower_limits,
            upperLimits=upper_limits,
            jointRanges=joint_ranges,
            restPoses=rest_poses,
            maxNumIterations=100,
            residualThreshold=1e-5,
            physicsClientId=self.loader.physics_client,
        )

        # Validate solution by checking distance to target
        # Set joints to solution
        for joint_idx in range(num_joints):
            p.resetJointState(
                pybullet_id,
                joint_idx,
                joint_angles[joint_idx],
                physicsClientId=self.loader.physics_client,
            )

        # Get actual end-effector position
        link_state = p.getLinkState(
            pybullet_id, num_joints, physicsClientId=self.loader.physics_client
        )
        actual_position = link_state[4]

        # Check if solution is close enough (within 1cm)
        distance = np.linalg.norm(np.array(actual_position) - np.array(target_position))
        if distance > 0.01:  # 1cm tolerance
            raise IKSolutionNotFoundError(robot_id, target_position)

        logger.debug(f"IK solution for {robot_id}: {joint_angles}, error={distance:.4f}m")

        return {
            "joint_angles": list(joint_angles[:num_joints]),  # Only return controllable joints
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
