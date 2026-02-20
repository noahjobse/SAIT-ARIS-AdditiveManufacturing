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
        if not self.loader.is_loaded(robot_id):
            self.loader.load_robot(robot_id)

        pybullet_id = self.loader.get_pybullet_id(robot_id)
        num_joints = self.loader.get_joint_count(robot_id)
        movable_indices = self.loader.get_movable_joint_indices(robot_id)
        ee_link = self.loader.get_ee_link_index(robot_id)

        if len(joint_angles) != num_joints:
            raise ValueError(f"Expected {num_joints} joint angles, got {len(joint_angles)}")

        self._validate_joint_limits(robot_id, joint_angles)

        # Set only movable joint positions
        for i, joint_idx in enumerate(movable_indices):
            p.resetJointState(
                pybullet_id,
                joint_idx,
                joint_angles[i],
                physicsClientId=self.loader.physics_client,
            )

        link_state = p.getLinkState(
            pybullet_id,
            ee_link,
            physicsClientId=self.loader.physics_client,
        )

        position = list(link_state[4])  # World position
        orientation = list(link_state[5])  # World orientation (quaternion)

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
        if not self.loader.is_loaded(robot_id):
            self.loader.load_robot(robot_id)

        pybullet_id = self.loader.get_pybullet_id(robot_id)
        num_joints = self.loader.get_joint_count(robot_id)
        movable_indices = self.loader.get_movable_joint_indices(robot_id)
        ee_link = self.loader.get_ee_link_index(robot_id)

        # Set current joints as starting position (if provided)
        if current_joints is not None:
            if len(current_joints) != num_joints:
                raise ValueError(
                    f"Expected {num_joints} current joints, got {len(current_joints)}"
                )
            for i, joint_idx in enumerate(movable_indices):
                p.resetJointState(
                    pybullet_id,
                    joint_idx,
                    current_joints[i],
                    physicsClientId=self.loader.physics_client,
                )

        # Get joint limits for PyBullet IK
        limits = self.loader.get_joint_limits(robot_id)
        lower_limits = [lim["lower"] for lim in limits]
        upper_limits = [lim["upper"] for lim in limits]
        joint_ranges = [upper - lower for upper, lower in zip(upper_limits, lower_limits)]
        rest_poses = [(upper + lower) / 2 for upper, lower in zip(upper_limits, lower_limits)]

        # Build IK kwargs
        ik_kwargs = {
            "bodyUniqueId": pybullet_id,
            "endEffectorLinkIndex": ee_link,
            "targetPosition": target_position,
            "lowerLimits": lower_limits,
            "upperLimits": upper_limits,
            "jointRanges": joint_ranges,
            "restPoses": rest_poses,
            "maxNumIterations": 100,
            "residualThreshold": 1e-5,
            "physicsClientId": self.loader.physics_client,
        }
        if target_orientation is not None:
            ik_kwargs["targetOrientation"] = target_orientation

        try:
            joint_angles = p.calculateInverseKinematics(**ik_kwargs)
        except p.error:
            raise IKSolutionNotFoundError(robot_id, target_position)

        # Validate solution: set joints and check distance to target
        for i, joint_idx in enumerate(movable_indices):
            p.resetJointState(
                pybullet_id,
                joint_idx,
                joint_angles[i],
                physicsClientId=self.loader.physics_client,
            )

        link_state = p.getLinkState(
            pybullet_id, ee_link, physicsClientId=self.loader.physics_client
        )
        actual_position = link_state[4]

        distance = np.linalg.norm(np.array(actual_position) - np.array(target_position))
        if distance > 0.01:  # 1cm tolerance
            raise IKSolutionNotFoundError(robot_id, target_position)

        return {
            "joint_angles": list(joint_angles[:num_joints]),
        }

    def _validate_joint_limits(self, robot_id: str, joint_angles: List[float]):
        """Validate joint angles against joint limits."""
        limits = self.loader.get_joint_limits(robot_id)

        for joint_idx, angle in enumerate(joint_angles):
            lower = limits[joint_idx]["lower"]
            upper = limits[joint_idx]["upper"]

            if angle < lower or angle > upper:
                raise InvalidJointAnglesError(
                    robot_id, joint_idx, angle, (lower, upper)
                )
