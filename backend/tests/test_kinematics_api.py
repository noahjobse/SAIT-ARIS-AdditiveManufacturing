"""Integration tests for kinematics API endpoints."""
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


class TestKinematicsAPI:
    """Test kinematics API endpoints."""

    def test_fk_endpoint_success(self):
        """Test FK endpoint with valid input."""
        response = client.post(
            "/api/kinematics/fk",
            json={
                "robot_id": "irb4600",
                "joint_angles": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert "position" in data
        assert "orientation" in data
        assert len(data["position"]) == 3
        assert len(data["orientation"]) == 4

    def test_fk_endpoint_invalid_joints(self):
        """Test FK endpoint with invalid joint count."""
        response = client.post(
            "/api/kinematics/fk",
            json={
                "robot_id": "irb4600",
                "joint_angles": [0.0, 0.0, 0.0],  # Only 3 joints
            },
        )

        assert response.status_code == 400
        assert "Expected 6 joint angles" in response.json()["detail"]

    def test_fk_endpoint_joint_limit_violation(self):
        """Test FK endpoint with joint limit violation."""
        response = client.post(
            "/api/kinematics/fk",
            json={
                "robot_id": "irb4600",
                "joint_angles": [10.0, 0.0, 0.0, 0.0, 0.0, 0.0],  # Way over limit
            },
        )

        assert response.status_code == 400
        assert "Invalid joint angles" in response.json()["detail"]

    def test_ik_endpoint_success(self):
        """Test IK endpoint with reachable target."""
        response = client.post(
            "/api/kinematics/ik",
            json={
                "robot_id": "irb4600",
                "target_position": [1.58, 0.0, 1.765],
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert "joint_angles" in data
        assert len(data["joint_angles"]) == 6

    def test_ik_endpoint_with_orientation(self):
        """Test IK endpoint with target orientation."""
        response = client.post(
            "/api/kinematics/ik",
            json={
                "robot_id": "irb4600",
                "target_position": [1.2, 0.3, 1.4],
                "target_orientation": [0, 0, 0, 1],
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data["joint_angles"]) == 6

    def test_ik_endpoint_unreachable(self):
        """Test IK endpoint with unreachable target."""
        response = client.post(
            "/api/kinematics/ik",
            json={
                "robot_id": "irb4600",
                "target_position": [10.0, 10.0, 10.0],  # Beyond reach
            },
        )

        assert response.status_code == 404
        assert "IK solution not found" in response.json()["detail"]

    def test_fk_ik_roundtrip(self):
        """Test FK -> IK -> FK round-trip consistency."""
        # FK with known joints
        fk_response = client.post(
            "/api/kinematics/fk",
            json={
                "robot_id": "irb4600",
                "joint_angles": [0.5, -0.3, 0.8, 0.0, 0.5, 0.0],
            },
        )
        assert fk_response.status_code == 200
        fk_data = fk_response.json()

        # IK to target pose
        ik_response = client.post(
            "/api/kinematics/ik",
            json={
                "robot_id": "irb4600",
                "target_position": fk_data["position"],
                "target_orientation": fk_data["orientation"],
            },
        )
        assert ik_response.status_code == 200
        ik_data = ik_response.json()

        # FK again to verify
        fk_verify = client.post(
            "/api/kinematics/fk",
            json={
                "robot_id": "irb4600",
                "joint_angles": ik_data["joint_angles"],
            },
        )
        assert fk_verify.status_code == 200
        verify_data = fk_verify.json()

        # Positions should match within tolerance
        for i in range(3):
            assert abs(verify_data["position"][i] - fk_data["position"][i]) < 0.01
