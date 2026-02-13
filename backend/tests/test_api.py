"""
Test API endpoints
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_endpoint():
    """Test that health check returns 200"""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data
    assert "timestamp" in data


def test_robots_endpoint():
    """Test that robots list returns 3 robots"""
    response = client.get("/api/robots")
    assert response.status_code == 200
    robots = response.json()

    # Should return 3 robots
    assert len(robots) == 3

    # Check IRB 4600
    assert robots[0]["id"] == "irb4600"
    assert robots[0]["name"] == "IRB 4600-60/2.05"
    assert robots[0]["manufacturer"] == "ABB"
    assert robots[0]["dof"] == 6
    assert robots[0]["payload_kg"] == 60
    assert robots[0]["reach_mm"] == 2050

    # Check IRB 2600
    assert robots[1]["id"] == "irb2600"
    assert robots[1]["payload_kg"] == 12

    # Check IRB 6700
    assert robots[2]["id"] == "irb6700"
    assert robots[2]["payload_kg"] == 145


def test_root_endpoint():
    """Test root endpoint returns project info"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data
    assert data["status"] == "running"
