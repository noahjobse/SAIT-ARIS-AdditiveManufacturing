"""Tests for robot URDF loading in PyBullet."""
import pytest
from pathlib import Path

from app.kinematics.robot_loader import RobotLoader
from app.kinematics.exceptions import RobotNotLoadedError


class TestRobotLoader:
    """Test robot loading functionality."""

    def test_load_irb4600_urdf(self):
        """Test loading IRB 4600 URDF into PyBullet."""
        loader = RobotLoader()
        robot_id = loader.load_robot("irb4600")

        assert robot_id is not None
        assert robot_id >= 0  # PyBullet returns non-negative IDs
        assert loader.is_loaded("irb4600")

        loader.disconnect()

    def test_get_joint_count(self):
        """Test getting joint count for loaded robot."""
        loader = RobotLoader()
        loader.load_robot("irb4600")

        joint_count = loader.get_joint_count("irb4600")
        assert joint_count == 6  # IRB 4600 has 6 DOF

        loader.disconnect()

    def test_get_joint_limits(self):
        """Test retrieving joint limits from URDF."""
        loader = RobotLoader()
        loader.load_robot("irb4600")

        limits = loader.get_joint_limits("irb4600")
        assert len(limits) == 6

        # Check joint 1 limits (base rotation: -180 to 180 degrees)
        assert limits[0]["lower"] == pytest.approx(-3.14159, abs=0.01)
        assert limits[0]["upper"] == pytest.approx(3.14159, abs=0.01)

        loader.disconnect()

    def test_robot_not_loaded_error(self):
        """Test error when accessing unloaded robot."""
        loader = RobotLoader()

        with pytest.raises(RobotNotLoadedError):
            loader.get_joint_count("nonexistent_robot")

        loader.disconnect()

    def test_urdf_file_missing(self):
        """Test handling of missing URDF file."""
        loader = RobotLoader()

        with pytest.raises(FileNotFoundError):
            loader.load_robot("missing_robot")

        loader.disconnect()

    def test_load_irb2600_urdf(self):
        """Test loading IRB 2600 URDF into PyBullet."""
        loader = RobotLoader()
        loader.load_robot("irb2600")

        assert loader.is_loaded("irb2600")
        assert loader.get_joint_count("irb2600") == 6

        limits = loader.get_joint_limits("irb2600")
        assert len(limits) == 6
        assert limits[0]["lower"] == pytest.approx(-3.14159, abs=0.01)

        loader.disconnect()

    def test_load_irb6700_urdf(self):
        """Test loading IRB 6700 URDF into PyBullet."""
        loader = RobotLoader()
        loader.load_robot("irb6700")

        assert loader.is_loaded("irb6700")
        assert loader.get_joint_count("irb6700") == 6

        limits = loader.get_joint_limits("irb6700")
        assert len(limits) == 6
        assert limits[0]["lower"] == pytest.approx(-2.967, abs=0.01)

        loader.disconnect()

    def test_fk_all_robots_zero_position(self):
        """Test FK at zero position for all 3 robots."""
        from app.kinematics.solver import KinematicsSolver

        solver = KinematicsSolver()
        zeros = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

        for robot_id in ["irb4600", "irb2600", "irb6700"]:
            result = solver.forward_kinematics(robot_id, zeros)
            assert len(result["position"]) == 3
            assert len(result["orientation"]) == 4
            # TCP should be in positive X (arm extended) and positive Z (above base)
            assert result["position"][0] > 0.5
            assert result["position"][2] > 0.3

        solver.disconnect()
