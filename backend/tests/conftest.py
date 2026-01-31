"""Shared test fixtures and configuration for ABB Robot Simulation Backend tests"""

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(scope="module")
def client():
    """Provides FastAPI TestClient for testing API endpoints.

    Module-scoped fixture for efficient reuse across test functions.
    """
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope="function")
def sample_robot_config():
    """Sample robot configuration data for testing.

    Returns a dict with typical robot configuration parameters
    that may be used in future robot setup or validation tests.
    """
    return {
        "robot_type": "IRB 4600",
        "dh_parameters": [
            {"a": 0.0, "alpha": 0.0, "d": 0.0, "theta": 0.0},
            {"a": 0.0, "alpha": -1.5708, "d": 0.0, "theta": 0.0},
            {"a": 0.9, "alpha": 0.0, "d": 0.0, "theta": 0.0},
            {"a": 0.7, "alpha": 1.5708, "d": 1.0, "theta": 0.0},
            {"a": 0.0, "alpha": -1.5708, "d": 1.0, "theta": 0.0},
            {"a": 0.0, "alpha": 1.5708, "d": 0.0, "theta": 0.0},
        ],
        "base_position": {"x": 0.0, "y": 0.0, "z": 0.0},
        "base_orientation": {"qx": 0.0, "qy": 0.0, "qz": 0.0, "qw": 1.0},
    }


@pytest.fixture(scope="function")
def sample_health_check_response():
    """Expected health check endpoint response structure.

    Returns the expected response from /health endpoint.
    """
    return {"status": "healthy"}


@pytest.fixture(scope="function")
def sample_root_response():
    """Expected root endpoint response structure.

    Returns the expected response from / endpoint with message,
    version, and status fields.
    """
    return {
        "message": "ABB Robot Simulation Backend",
        "version": "0.1.0",
        "status": "running",
    }
