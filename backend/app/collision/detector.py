"""Collision detection between robot and obstacles using PyBullet."""
import logging
from pathlib import Path

import pybullet as p

from app.kinematics.robot_loader import RobotLoader

logger = logging.getLogger(__name__)


class CollisionDetector:
    """Detects collisions between a robot and obstacle meshes using PyBullet."""

    def __init__(self, loader: RobotLoader | None = None):
        """
        Initialize collision detector.

        Args:
            loader: Existing RobotLoader to share PyBullet connection.
                    Creates a new one if not provided.
        """
        self.loader = loader or RobotLoader(headless=True)
        self.obstacles: dict[str, int] = {}  # obstacle_id -> pybullet_body_id

    def disconnect(self):
        """Disconnect from PyBullet."""
        self.loader.disconnect()

    def load_obstacle(
        self,
        obstacle_id: str,
        stl_path: str,
        position: list[float] = None,
        orientation: list[float] = None,
    ) -> int:
        """
        Load an obstacle STL into PyBullet.

        Args:
            obstacle_id: Unique identifier for the obstacle
            stl_path: Path to the STL file
            position: [x, y, z] in meters (default: origin)
            orientation: [qx, qy, qz, qw] quaternion (default: identity)

        Returns:
            PyBullet body ID

        Raises:
            FileNotFoundError: If STL file not found
        """
        stl = Path(stl_path)
        if not stl.exists():
            raise FileNotFoundError(f"STL file not found: {stl_path}")

        position = position or [0, 0, 0]
        orientation = orientation or [0, 0, 0, 1]

        # Create collision shape from STL mesh
        collision_shape = p.createCollisionShape(
            p.GEOM_MESH,
            fileName=str(stl),
            meshScale=[1, 1, 1],
            physicsClientId=self.loader.physics_client,
        )

        # Create multi-body with the collision shape
        body_id = p.createMultiBody(
            baseMass=0,  # Static obstacle
            baseCollisionShapeIndex=collision_shape,
            basePosition=position,
            baseOrientation=orientation,
            physicsClientId=self.loader.physics_client,
        )

        self.obstacles[obstacle_id] = body_id
        logger.info(f"Loaded obstacle '{obstacle_id}' (body ID: {body_id})")
        return body_id

    def remove_obstacle(self, obstacle_id: str):
        """Remove an obstacle from PyBullet."""
        if obstacle_id in self.obstacles:
            p.removeBody(
                self.obstacles[obstacle_id],
                physicsClientId=self.loader.physics_client,
            )
            del self.obstacles[obstacle_id]

    def check_collisions(
        self,
        robot_id: str,
        joint_angles: list[float],
        distance_threshold: float = 0.0,
    ) -> list[dict]:
        """
        Check for collisions between robot and all loaded obstacles.

        Args:
            robot_id: Robot identifier
            joint_angles: Current joint angles in radians
            distance_threshold: Contact distance threshold in meters.
                                0.0 = touching, negative = penetrating.

        Returns:
            List of collision dicts with keys:
                obstacle_id, link_index, contact_point, penetration_depth
        """
        if not self.loader.is_loaded(robot_id):
            self.loader.load_robot(robot_id)

        pybullet_id = self.loader.get_pybullet_id(robot_id)
        movable_indices = self.loader.get_movable_joint_indices(robot_id)

        # Set robot to specified joint configuration
        for i, joint_idx in enumerate(movable_indices):
            p.resetJointState(
                pybullet_id,
                joint_idx,
                joint_angles[i],
                physicsClientId=self.loader.physics_client,
            )

        # Step simulation to update collision state
        p.performCollisionDetection(physicsClientId=self.loader.physics_client)

        collisions = []
        for obstacle_id, obstacle_body_id in self.obstacles.items():
            contacts = p.getClosestPoints(
                pybullet_id,
                obstacle_body_id,
                distance=distance_threshold,
                physicsClientId=self.loader.physics_client,
            )

            for contact in contacts:
                collisions.append({
                    "obstacle_id": obstacle_id,
                    "link_index": contact[3],  # Link index on robot
                    "contact_point": list(contact[5]),  # Position on obstacle
                    "penetration_depth": -contact[8],  # Negative = penetration
                })

        return collisions

    def check_trajectory_collisions(
        self,
        robot_id: str,
        trajectory: list[list[float]],
        distance_threshold: float = 0.0,
    ) -> list[dict]:
        """
        Check collisions for each waypoint in a trajectory.

        Args:
            robot_id: Robot identifier
            trajectory: List of joint angle arrays
            distance_threshold: Contact distance threshold

        Returns:
            List of dicts with 'waypoint_index' and 'collisions' for each collision
        """
        results = []
        for idx, joint_angles in enumerate(trajectory):
            collisions = self.check_collisions(
                robot_id, joint_angles, distance_threshold
            )
            if collisions:
                results.append({
                    "waypoint_index": idx,
                    "collisions": collisions,
                })
        return results
