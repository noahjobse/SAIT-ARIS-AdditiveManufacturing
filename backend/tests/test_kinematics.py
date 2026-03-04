"""Tests for kinematics FK/IK solvers."""
import numpy as np
import pytest

from app.kinematics.exceptions import IKSolutionNotFoundError, InvalidJointAnglesError
from app.kinematics.solver import KinematicsSolver


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


class TestInverseKinematics:
    """Test inverse kinematics calculations."""

    def test_ik_simple_target(self):
        """Test IK for reachable target position."""
        solver = KinematicsSolver()

        # Target at home position (should return close to zero angles)
        target_position = [1.58, 0.0, 1.765]
        target_orientation = None  # Use default orientation

        result = solver.inverse_kinematics(
            "irb4600", target_position, target_orientation
        )

        assert "joint_angles" in result
        assert len(result["joint_angles"]) == 6

        # Verify solution by running FK
        fk_result = solver.forward_kinematics("irb4600", result["joint_angles"])
        assert fk_result["position"][0] == pytest.approx(target_position[0], abs=0.01)
        assert fk_result["position"][1] == pytest.approx(target_position[1], abs=0.01)
        assert fk_result["position"][2] == pytest.approx(target_position[2], abs=0.01)

        solver.disconnect()

    def test_ik_with_orientation(self):
        """Test IK with target position and orientation."""
        solver = KinematicsSolver()

        target_position = [1.0, 0.5, 1.5]
        target_orientation = [0, 0, 0, 1]  # Identity quaternion

        result = solver.inverse_kinematics(
            "irb4600", target_position, target_orientation
        )

        assert len(result["joint_angles"]) == 6

        # Verify with FK
        fk_result = solver.forward_kinematics("irb4600", result["joint_angles"])
        np.testing.assert_allclose(
            fk_result["position"], target_position, atol=0.01
        )

        solver.disconnect()

    def test_ik_unreachable_target(self):
        """Test IK for unreachable target (too far)."""
        solver = KinematicsSolver()

        # Target beyond robot reach (reach is ~2.05m)
        target_position = [5.0, 0.0, 0.0]

        with pytest.raises(IKSolutionNotFoundError):
            solver.inverse_kinematics("irb4600", target_position)

        solver.disconnect()

    def test_ik_fk_roundtrip(self):
        """Test FK(IK(pose)) ≈ pose round-trip."""
        solver = KinematicsSolver()

        # Start with known joint angles
        original_angles = [0.5, -0.3, 0.8, 0.0, 0.5, 0.0]

        # FK to get pose
        fk_result = solver.forward_kinematics("irb4600", original_angles)

        # IK back to joint angles
        ik_result = solver.inverse_kinematics(
            "irb4600",
            fk_result["position"],
            fk_result["orientation"]
        )

        # FK again to verify
        fk_verify = solver.forward_kinematics("irb4600", ik_result["joint_angles"])

        np.testing.assert_allclose(
            fk_verify["position"], fk_result["position"], atol=0.01
        )

        solver.disconnect()

    def test_ik_with_current_joints_hint(self):
        """Test IK with current joint angles as seed."""
        solver = KinematicsSolver()

        target_position = [1.2, 0.3, 1.4]
        current_joints = [0.1, -0.2, 0.3, 0.0, 0.2, 0.0]

        result = solver.inverse_kinematics(
            "irb4600",
            target_position,
            current_joints=current_joints
        )

        assert len(result["joint_angles"]) == 6

        solver.disconnect()
