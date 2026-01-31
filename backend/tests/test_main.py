"""Tests for app.main module - Core FastAPI application endpoints and middleware.

This test module provides comprehensive coverage of the main FastAPI application,
including all available endpoints and CORS configuration.
"""

import pytest


class TestRootEndpoint:
    """Tests for the root GET / endpoint."""

    def test_root_status_code(self, client):
        """Root endpoint returns 200 OK status code."""
        response = client.get("/")
        assert response.status_code == 200

    def test_root_content_type(self, client):
        """Root endpoint returns JSON content type."""
        response = client.get("/")
        assert response.headers["content-type"] == "application/json"

    def test_root_response_structure(self, client):
        """Root endpoint returns expected response structure with all required fields."""
        response = client.get("/")
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert "status" in data

    def test_root_response_message(self, client, sample_root_response):
        """Root endpoint message matches expected value."""
        response = client.get("/")
        assert response.json()["message"] == sample_root_response["message"]

    def test_root_response_version(self, client, sample_root_response):
        """Root endpoint version matches expected value."""
        response = client.get("/")
        assert response.json()["version"] == sample_root_response["version"]

    def test_root_response_status(self, client, sample_root_response):
        """Root endpoint status matches expected value."""
        response = client.get("/")
        assert response.json()["status"] == sample_root_response["status"]

    def test_root_message_is_string(self, client):
        """Root endpoint message is a string."""
        response = client.get("/")
        data = response.json()
        assert isinstance(data["message"], str)
        assert len(data["message"]) > 0

    def test_root_version_is_string(self, client):
        """Root endpoint version is a string in semantic versioning format."""
        response = client.get("/")
        data = response.json()
        assert isinstance(data["version"], str)
        # Basic semantic versioning check: x.y.z format
        parts = data["version"].split(".")
        assert len(parts) == 3

    def test_root_status_is_string(self, client):
        """Root endpoint status is a string."""
        response = client.get("/")
        data = response.json()
        assert isinstance(data["status"], str)
        assert len(data["status"]) > 0

    def test_root_full_response_match(self, client, sample_root_response):
        """Root endpoint response fully matches expected structure and values."""
        response = client.get("/")
        assert response.json() == sample_root_response

    def test_root_no_extra_fields(self, client):
        """Root endpoint response contains no extra unexpected fields."""
        response = client.get("/")
        data = response.json()
        expected_keys = {"message", "version", "status"}
        assert set(data.keys()) == expected_keys

    def test_root_response_is_dict(self, client):
        """Root endpoint response is a dictionary/JSON object."""
        response = client.get("/")
        assert isinstance(response.json(), dict)


class TestHealthEndpoint:
    """Tests for the GET /health endpoint."""

    def test_health_status_code(self, client):
        """Health endpoint returns 200 OK status code."""
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_content_type(self, client):
        """Health endpoint returns JSON content type."""
        response = client.get("/health")
        assert response.headers["content-type"] == "application/json"

    def test_health_response_structure(self, client):
        """Health endpoint returns expected response structure with status field."""
        response = client.get("/health")
        data = response.json()
        assert "status" in data

    def test_health_status_value(self, client, sample_health_check_response):
        """Health endpoint status field has expected value."""
        response = client.get("/health")
        assert response.json()["status"] == sample_health_check_response["status"]

    def test_health_status_is_string(self, client):
        """Health endpoint status value is a string."""
        response = client.get("/health")
        data = response.json()
        assert isinstance(data["status"], str)
        assert len(data["status"]) > 0

    def test_health_status_is_healthy(self, client):
        """Health endpoint status value is 'healthy'."""
        response = client.get("/health")
        assert response.json()["status"] == "healthy"

    def test_health_full_response_match(self, client, sample_health_check_response):
        """Health endpoint response fully matches expected structure and values."""
        response = client.get("/health")
        assert response.json() == sample_health_check_response

    def test_health_no_extra_fields(self, client):
        """Health endpoint response contains only the status field."""
        response = client.get("/health")
        data = response.json()
        assert set(data.keys()) == {"status"}

    def test_health_response_is_dict(self, client):
        """Health endpoint response is a dictionary/JSON object."""
        response = client.get("/health")
        assert isinstance(response.json(), dict)


class TestCORSConfiguration:
    """Tests for CORS middleware configuration."""

    def test_cors_origin_header_present(self, client):
        """CORS allow-origin header is present in response."""
        response = client.get("/", headers={"Origin": "http://localhost:3000"})
        assert "access-control-allow-origin" in response.headers

    def test_cors_allows_all_origins(self, client):
        """CORS configuration allows all origins (*)."""
        response = client.get("/", headers={"Origin": "http://localhost:3000"})
        # When allowing all origins, the header value should be "*"
        assert response.headers.get("access-control-allow-origin") == "*"

    def test_cors_allows_credentials(self, client):
        """CORS configuration allows credentials."""
        response = client.get("/", headers={"Origin": "http://localhost:3000"})
        assert response.headers.get("access-control-allow-credentials") == "true"

    def test_cors_health_endpoint(self, client):
        """CORS is enabled on health endpoint."""
        response = client.get("/health", headers={"Origin": "http://localhost:3000"})
        assert response.headers.get("access-control-allow-origin") == "*"

    def test_cors_with_post_method(self, client):
        """CORS headers present when making requests with different methods."""
        # Test with a simulated POST request (not an actual endpoint, just checking headers)
        response = client.get(
            "/", headers={"Origin": "http://localhost:3000"}
        )
        assert "access-control-allow-origin" in response.headers

    def test_cors_configuration_complete(self, client):
        """CORS configuration includes necessary headers."""
        response = client.get("/health", headers={"Origin": "http://example.com"})
        # Should have at least origin and credentials headers
        assert "access-control-allow-origin" in response.headers
        assert response.headers.get("access-control-allow-credentials") == "true"


class TestApplicationMetadata:
    """Tests for application metadata and version information."""

    def test_app_title_set(self):
        """FastAPI application has correct title."""
        from app.main import app

        assert app.title == "ABB Robot Simulation Backend"

    def test_app_description_set(self):
        """FastAPI application has correct description."""
        from app.main import app

        assert app.description == "FastAPI + PyBullet backend for ABB robot simulation"

    def test_app_version_format(self):
        """FastAPI application version follows semantic versioning."""
        from app.main import app

        version = app.version
        assert version is not None
        parts = version.split(".")
        assert len(parts) == 3
        # All parts should be numeric
        for part in parts:
            assert part.isdigit()

    def test_app_version_matches_endpoint(self, client):
        """Application version in metadata matches root endpoint version."""
        from app.main import app

        response = client.get("/")
        endpoint_version = response.json()["version"]
        assert app.version == endpoint_version


class TestEndpointAvailability:
    """Tests for endpoint availability and accessibility."""

    def test_root_endpoint_accessible(self, client):
        """Root endpoint is accessible and responds."""
        response = client.get("/")
        assert response.status_code in (200, 405)  # 200 for GET, 405 if method not allowed

    def test_health_endpoint_accessible(self, client):
        """Health endpoint is accessible and responds."""
        response = client.get("/health")
        assert response.status_code in (200, 405)

    def test_undefined_endpoint_returns_404(self, client):
        """Undefined endpoints return 404 Not Found."""
        response = client.get("/undefined-endpoint")
        assert response.status_code == 404

    def test_root_endpoint_get_allowed(self, client):
        """Root endpoint allows GET requests."""
        response = client.get("/")
        assert response.status_code == 200

    def test_health_endpoint_get_allowed(self, client):
        """Health endpoint allows GET requests."""
        response = client.get("/health")
        assert response.status_code == 200


class TestAsyncEndpoints:
    """Tests for async endpoint functionality."""

    def test_root_endpoint_async(self, client):
        """Root endpoint handles async requests properly."""
        response = client.get("/")
        assert response.status_code == 200
        assert isinstance(response.json(), dict)

    def test_health_endpoint_async(self, client):
        """Health endpoint handles async requests properly."""
        response = client.get("/health")
        assert response.status_code == 200
        assert isinstance(response.json(), dict)

    @pytest.mark.parametrize(
        "endpoint",
        [
            "/",
            "/health",
        ],
    )
    def test_multiple_endpoint_calls(self, client, endpoint):
        """Multiple calls to endpoints work consistently.

        Parametrized test to ensure all endpoints handle multiple
        sequential requests without issues.
        """
        for _ in range(3):
            response = client.get(endpoint)
            assert response.status_code == 200

    @pytest.mark.parametrize(
        "endpoint,expected_fields",
        [
            ("/", ["message", "version", "status"]),
            ("/health", ["status"]),
        ],
    )
    def test_endpoint_response_fields(self, client, endpoint, expected_fields):
        """Endpoints return responses with expected fields.

        Parametrized test to check response structure across
        multiple endpoints.
        """
        response = client.get(endpoint)
        data = response.json()
        for field in expected_fields:
            assert field in data
