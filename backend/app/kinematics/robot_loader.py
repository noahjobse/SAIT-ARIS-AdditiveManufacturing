"""Robot URDF loader for PyBullet."""
import json
import logging
from pathlib import Path
from typing import Dict, Optional

import pybullet as p
import pybullet_data

from .exceptions import RobotNotLoadedError

logger = logging.getLogger(__name__)


class RobotLoader:
    """Manages loading and tracking robots in PyBullet."""

    def __init__(self, headless: bool = True):
        """
        Initialize PyBullet connection and robot tracking.

        Args:
            headless: If True, run PyBullet in DIRECT mode (no GUI)
        """
        self.headless = headless
        self.physics_client = None
        self.loaded_robots: Dict[str, int] = {}  # robot_id -> pybullet_id
        self.robot_configs: Dict[str, dict] = {}  # robot_id -> config
        self._movable_joints: Dict[str, list] = {}  # robot_id -> [joint indices]
        self._ee_link_index: Dict[str, int] = {}  # robot_id -> end-effector link index
        self.connect()

    def connect(self):
        """Establish PyBullet connection."""
        if self.physics_client is None:
            if self.headless:
                self.physics_client = p.connect(p.DIRECT)
            else:
                self.physics_client = p.connect(p.GUI)

            p.setAdditionalSearchPath(pybullet_data.getDataPath())
            logger.info(f"PyBullet connected (headless={self.headless})")

    def disconnect(self):
        """Disconnect from PyBullet."""
        if self.physics_client is not None:
            p.disconnect(self.physics_client)
            self.physics_client = None
            self.loaded_robots.clear()
            self.robot_configs.clear()
            self._movable_joints.clear()
            self._ee_link_index.clear()
            logger.info("PyBullet disconnected")

    def load_robot(self, robot_id: str) -> int:
        """
        Load a robot URDF into PyBullet.

        Args:
            robot_id: Robot identifier (e.g., 'irb4600')

        Returns:
            PyBullet robot body ID

        Raises:
            FileNotFoundError: If URDF or config file not found
        """
        if robot_id in self.loaded_robots:
            logger.info(f"Robot '{robot_id}' already loaded")
            return self.loaded_robots[robot_id]

        # Load config
        config_path = self._get_config_path(robot_id)
        if not config_path.exists():
            raise FileNotFoundError(f"Config file not found: {config_path}")

        with open(config_path, "r") as f:
            config = json.load(f)

        # Load URDF
        urdf_path = self._get_urdf_path(robot_id, config)
        if not urdf_path.exists():
            raise FileNotFoundError(f"URDF file not found: {urdf_path}")

        # Load into PyBullet
        pybullet_id = p.loadURDF(
            str(urdf_path),
            basePosition=[0, 0, 0],
            baseOrientation=[0, 0, 0, 1],
            useFixedBase=True,
            physicsClientId=self.physics_client,
        )

        self.loaded_robots[robot_id] = pybullet_id
        self.robot_configs[robot_id] = config

        # Discover movable (revolute/prismatic) joints vs fixed joints
        total_joints = p.getNumJoints(pybullet_id, physicsClientId=self.physics_client)
        movable = []
        ee_index = total_joints - 1  # Default to last joint's child link
        for i in range(total_joints):
            info = p.getJointInfo(pybullet_id, i, physicsClientId=self.physics_client)
            joint_type = info[2]
            if joint_type != p.JOINT_FIXED:
                movable.append(i)
            else:
                # The fixed joint's link is likely the end-effector
                ee_index = i

        self._movable_joints[robot_id] = movable
        self._ee_link_index[robot_id] = ee_index
        logger.info(
            f"Loaded robot '{robot_id}' (PyBullet ID: {pybullet_id}, "
            f"{len(movable)} movable joints, EE link: {ee_index})"
        )

        return pybullet_id

    def is_loaded(self, robot_id: str) -> bool:
        """Check if a robot is loaded."""
        return robot_id in self.loaded_robots

    def get_pybullet_id(self, robot_id: str) -> int:
        """Get PyBullet body ID for a loaded robot."""
        if robot_id not in self.loaded_robots:
            raise RobotNotLoadedError(robot_id)
        return self.loaded_robots[robot_id]

    def get_joint_count(self, robot_id: str) -> int:
        """Get number of movable joints for a robot."""
        self.get_pybullet_id(robot_id)  # Validate robot is loaded
        return len(self._movable_joints[robot_id])

    def get_movable_joint_indices(self, robot_id: str) -> list:
        """Get PyBullet indices of movable joints."""
        self.get_pybullet_id(robot_id)  # Validate robot is loaded
        return self._movable_joints[robot_id]

    def get_ee_link_index(self, robot_id: str) -> int:
        """Get PyBullet link index for the end-effector (tool0)."""
        self.get_pybullet_id(robot_id)  # Validate robot is loaded
        return self._ee_link_index[robot_id]

    def get_joint_limits(self, robot_id: str) -> list:
        """
        Get joint limits for movable joints only.

        Returns:
            List of dicts with 'lower', 'upper', 'velocity' for each movable joint
        """
        pybullet_id = self.get_pybullet_id(robot_id)

        limits = []
        for joint_idx in self._movable_joints[robot_id]:
            joint_info = p.getJointInfo(
                pybullet_id, joint_idx, physicsClientId=self.physics_client
            )
            limits.append({
                "lower": joint_info[8],   # Lower limit
                "upper": joint_info[9],   # Upper limit
                "velocity": joint_info[11],  # Max velocity
                "effort": joint_info[10],    # Max effort
            })

        return limits

    def _get_config_path(self, robot_id: str) -> Path:
        """Get path to robot config.json file."""
        return Path(__file__).parents[3] / "models" / "robots" / robot_id / "config.json"

    def _get_urdf_path(self, robot_id: str, config: dict) -> Path:
        """Get path to URDF file from config."""
        urdf_relative = config.get("urdf_path")
        if not urdf_relative:
            raise ValueError(f"No 'urdf_path' in config for robot '{robot_id}'")

        return Path(__file__).parents[3] / urdf_relative
