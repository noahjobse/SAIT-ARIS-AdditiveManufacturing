"""Tests for collision detection module."""
import struct

import pytest

from app.collision.detector import CollisionDetector


def create_test_stl(path: str):
    """Create a minimal binary STL cube for testing."""
    # Simple cube centered at origin, 0.5m sides
    vertices = [
        # Front face
        ((-0.25, -0.25, -0.25), (-0.25, 0.25, -0.25), (0.25, 0.25, -0.25)),
        ((-0.25, -0.25, -0.25), (0.25, 0.25, -0.25), (0.25, -0.25, -0.25)),
        # Back face
        ((-0.25, -0.25, 0.25), (0.25, 0.25, 0.25), (-0.25, 0.25, 0.25)),
        ((-0.25, -0.25, 0.25), (0.25, -0.25, 0.25), (0.25, 0.25, 0.25)),
        # Top face
        ((-0.25, 0.25, -0.25), (-0.25, 0.25, 0.25), (0.25, 0.25, 0.25)),
        ((-0.25, 0.25, -0.25), (0.25, 0.25, 0.25), (0.25, 0.25, -0.25)),
        # Bottom face
        ((-0.25, -0.25, -0.25), (0.25, -0.25, 0.25), (-0.25, -0.25, 0.25)),
        ((-0.25, -0.25, -0.25), (0.25, -0.25, -0.25), (0.25, -0.25, 0.25)),
        # Left face
        ((-0.25, -0.25, -0.25), (-0.25, -0.25, 0.25), (-0.25, 0.25, 0.25)),
        ((-0.25, -0.25, -0.25), (-0.25, 0.25, 0.25), (-0.25, 0.25, -0.25)),
        # Right face
        ((0.25, -0.25, -0.25), (0.25, 0.25, 0.25), (0.25, -0.25, 0.25)),
        ((0.25, -0.25, -0.25), (0.25, 0.25, -0.25), (0.25, 0.25, 0.25)),
    ]

    with open(path, "wb") as f:
        f.write(b"\0" * 80)  # Header
        f.write(struct.pack("<I", len(vertices)))  # Triangle count
        for v1, v2, v3 in vertices:
            f.write(struct.pack("<fff", 0, 0, 0))  # Normal (auto-calculated)
            f.write(struct.pack("<fff", *v1))
            f.write(struct.pack("<fff", *v2))
            f.write(struct.pack("<fff", *v3))
            f.write(struct.pack("<H", 0))  # Attribute byte count


class TestCollisionDetector:
    """Test collision detection functionality."""

    def test_load_obstacle(self, tmp_path):
        """Test loading an STL obstacle."""
        stl_file = str(tmp_path / "cube.stl")
        create_test_stl(stl_file)

        detector = CollisionDetector()
        body_id = detector.load_obstacle("test_cube", stl_file, position=[2, 0, 0])

        assert body_id >= 0
        assert "test_cube" in detector.obstacles

        detector.disconnect()

    def test_load_obstacle_missing_file(self):
        """Test error when STL file doesn't exist."""
        detector = CollisionDetector()

        with pytest.raises(FileNotFoundError):
            detector.load_obstacle("missing", "/nonexistent/file.stl")

        detector.disconnect()

    def test_no_collision_at_home(self, tmp_path):
        """Test no collision when obstacle is far from robot."""
        stl_file = str(tmp_path / "cube.stl")
        create_test_stl(stl_file)

        detector = CollisionDetector()
        detector.loader.load_robot("irb4600")
        # Place obstacle far away
        detector.load_obstacle("far_cube", stl_file, position=[10, 10, 10])

        collisions = detector.check_collisions(
            "irb4600", [0, 0, 0, 0, 0, 0]
        )
        assert len(collisions) == 0

        detector.disconnect()

    def test_collision_detected(self, tmp_path):
        """Test collision when obstacle overlaps robot."""
        stl_file = str(tmp_path / "cube.stl")
        create_test_stl(stl_file)

        detector = CollisionDetector()
        detector.loader.load_robot("irb4600")
        # Place obstacle at robot's home TCP position (should collide)
        detector.load_obstacle("overlap_cube", stl_file, position=[1.5, 0, 1.7])

        collisions = detector.check_collisions(
            "irb4600", [0, 0, 0, 0, 0, 0]
        )
        assert len(collisions) > 0
        assert collisions[0]["obstacle_id"] == "overlap_cube"

        detector.disconnect()

    def test_remove_obstacle(self, tmp_path):
        """Test removing an obstacle."""
        stl_file = str(tmp_path / "cube.stl")
        create_test_stl(stl_file)

        detector = CollisionDetector()
        detector.load_obstacle("temp", stl_file)
        assert "temp" in detector.obstacles

        detector.remove_obstacle("temp")
        assert "temp" not in detector.obstacles

        detector.disconnect()

    def test_trajectory_collisions(self, tmp_path):
        """Test collision checking across a trajectory."""
        stl_file = str(tmp_path / "cube.stl")
        create_test_stl(stl_file)

        detector = CollisionDetector()
        detector.loader.load_robot("irb4600")
        # Place obstacle at TCP home position
        detector.load_obstacle("traj_cube", stl_file, position=[1.5, 0, 1.7])

        trajectory = [
            [0, 0, 0, 0, 0, 0],       # Home - should collide
            [1.5, 0, 0, 0, 0, 0],     # Rotated away - might not collide
        ]

        results = detector.check_trajectory_collisions("irb4600", trajectory)
        # At least the home position should have collisions
        assert len(results) > 0
        assert results[0]["waypoint_index"] == 0

        detector.disconnect()
