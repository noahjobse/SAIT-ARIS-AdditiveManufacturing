"""Tests for kinematics FK/IK solvers."""
import pytest
import numpy as np

from app.kinematics.solver import KinematicsSolver
from app.kinematics.exceptions import InvalidJointAnglesError


class TestForwardKinematics:
    """Test forward kinematics calculations."""

    def test_fk_zero_position(self):
        """Test FK at zero (home) position."""
        solver = KinematicsSolver()

        joint_angles = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        result = solver.forward_kinematics("irb4600", joint_angles)

        assert "position" in result
        assert "orientation" in result
        assert len(result["position"]) == 3
        assert len(result["orientation"]) == 4  # Quaternion

        # At zero position, TCP should be at approximately [1.58, 0, 1.765]
        # (sum of link offsets: 0.175 + 1.270 + 0.135 = 1.58 in X)
        # (base height + link2 offset: 0.495 + 1.095 + 0.175 = 1.765 in Z)
        assert result["position"][0] == pytest.approx(1.58, abs=0.01)
        assert result["position"][1] == pytest.approx(0.0, abs=0.01)
        assert result["position"][2] == pytest.approx(1.765, abs=0.01)

        solver.disconnect()

    def test_fk_custom_position(self):
        """Test FK at non-zero joint angles."""
        solver = KinematicsSolver()

        # 90 degree rotation on joint 1 (base)
        joint_angles = [1.5708, 0.0, 0.0, 0.0, 0.0, 0.0]  # 90 degrees in radians
        result = solver.forward_kinematics("irb4600", joint_angles)

        # After 90° rotation, X should be ~0, Y should be ~1.58
        assert result["position"][0] == pytest.approx(0.0, abs=0.01)
        assert result["position"][1] == pytest.approx(1.58, abs=0.01)

        solver.disconnect()

    def test_fk_invalid_joint_count(self):
        """Test FK with wrong number of joints."""
        solver = KinematicsSolver()

        with pytest.raises(ValueError, match="Expected 6 joint angles"):
            solver.forward_kinematics("irb4600", [0.0, 0.0, 0.0])

        solver.disconnect()

    def test_fk_joint_limits_violation(self):
        """Test FK with joint angles outside limits."""
        solver = KinematicsSolver()

        # Joint 1 limit is ±180° (-3.14 to 3.14), try 400° (6.98 rad)
        with pytest.raises(InvalidJointAnglesError):
            solver.forward_kinematics("irb4600", [7.0, 0.0, 0.0, 0.0, 0.0, 0.0])

        solver.disconnect()
