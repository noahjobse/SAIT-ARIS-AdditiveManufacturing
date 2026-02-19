"""
Test robot endpoints
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_get_robot_model_irb4600():
    """Test getting IRB 4600 GLB model"""
    response = client.get("/api/robots/irb4600/model")

    # Should return the GLB file
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/octet-stream"

    # Check file is not empty
    content = response.content
    assert len(content) > 0

    # Check it's a valid glTF binary (starts with "glTF" magic)
    assert content[:4] == b"glTF"


def test_get_robot_model_invalid_id():
    """Test getting model with invalid robot ID"""
    response = client.get("/api/robots/invalid_robot/model")

    assert response.status_code == 404
    assert "Invalid robot ID" in response.json()["detail"]


def test_get_robot_model_irb2600():
    """Test getting IRB 2600 GLB model"""
    response = client.get("/api/robots/irb2600/model")

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/octet-stream"
    assert response.content[:4] == b"glTF"


def test_get_robot_model_irb6700():
    """Test getting IRB 6700 GLB model"""
    response = client.get("/api/robots/irb6700/model")

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/octet-stream"
    assert response.content[:4] == b"glTF"
