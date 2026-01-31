# Backend Testing Guide

This guide provides comprehensive documentation for the pytest-based testing infrastructure for the ABB Robot Simulation Backend.

## Table of Contents

1. [Overview](#overview)
2. [Quick Start](#quick-start)
3. [Test Structure](#test-structure)
4. [Writing Tests](#writing-tests)
5. [Running Tests](#running-tests)
6. [Coverage Requirements](#coverage-requirements)
7. [Best Practices](#best-practices)
8. [Common Patterns](#common-patterns)
9. [Troubleshooting](#troubleshooting)
10. [Advanced Topics](#advanced-topics)
11. [Checklist for New Tests](#checklist-for-new-tests)

## Overview

The backend testing infrastructure uses **pytest** as the testing framework with the following components:

- **pytest**: Main testing framework
- **pytest-asyncio**: Async test support for FastAPI async endpoints
- **pytest-cov**: Coverage reporting and enforcement
- **TestClient (fastapi.testclient)**: HTTP client for API testing

### Why These Tools?

- **pytest**: Standard Python testing framework with excellent fixture support and plugin ecosystem
- **pytest-asyncio**: Native support for async/await test code without boilerplate
- **pytest-cov**: Integrated coverage reporting with HTML reports for detailed analysis
- **TestClient**: Official FastAPI testing client, handles ASGI applications correctly

### Coverage Requirements

- **Minimum Coverage**: 70% of backend code must be covered by tests
- **Enforcement**: CI/CD pipeline fails builds below 70% coverage
- **Reporting**: HTML reports available locally, XML reports uploaded to Codecov

## Quick Start

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

This installs pytest, pytest-asyncio, and pytest-cov.

### 2. Run All Tests

```bash
cd backend
pytest -v
```

Output shows:
- All test names and results
- Pass/fail/skip status
- Execution time
- Coverage summary

### 3. Run with Coverage Report

```bash
cd backend
pytest --cov=app --cov-report=term-missing
```

Shows:
- Coverage percentage for each file
- Line numbers of uncovered code
- Total project coverage

### 4. Generate HTML Coverage Report

```bash
cd backend
pytest --cov=app --cov-report=html
open htmlcov/index.html  # macOS
# OR
start htmlcov/index.html  # Windows
```

Displays:
- Interactive coverage report
- Click files to see highlighted coverage
- Missing lines clearly marked

### 5. Run Specific Test

```bash
cd backend
pytest tests/test_main.py::TestRootEndpoint::test_root_status_code -v
```

## Test Structure

### Directory Layout

```
backend/
├── tests/
│   ├── __init__.py                 # Package marker
│   ├── conftest.py                 # Shared fixtures
│   ├── test_main.py                # Tests for app/main.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── .gitkeep
│   ├── services/
│   │   ├── __init__.py
│   │   └── .gitkeep
│   ├── models/
│   │   ├── __init__.py
│   │   └── .gitkeep
│   └── core/
│       ├── __init__.py
│       └── .gitkeep
└── app/
    └── main.py                     # Application code
```

### Directory Purpose

- **tests/__init__.py**: Marks tests/ as a package
- **tests/conftest.py**: Shared fixtures used across test files
- **tests/test_main.py**: Tests for app/main.py endpoints and middleware
- **tests/api/**: Future tests for API routers and endpoints
- **tests/services/**: Future tests for business logic services
- **tests/models/**: Future tests for data models and validation
- **tests/core/**: Future tests for core utilities and configuration

### Test Naming Conventions

- **File names**: `test_*.py` - pytest automatically discovers these
- **Class names**: `Test*` - groups related tests together
- **Function names**: `test_*` - each function is an individual test
- **Descriptive names**: Use clear English descriptions (avoid abbreviated names)

### Example Naming

```python
# Good
class TestRootEndpoint:
    def test_root_status_code_is_200(self, client):
        ...

# Avoid
class TestRoot:
    def test_status(self, client):
        ...
```

## Writing Tests

### Basic Test Structure

```python
"""Module docstring with purpose of tests"""

class TestFeatureName:
    """Test class for a specific feature."""

    def test_specific_behavior(self, client):
        """Descriptive docstring of what is being tested."""
        # Arrange: Set up test data
        endpoint = "/health"

        # Act: Perform the action being tested
        response = client.get(endpoint)

        # Assert: Verify the results
        assert response.status_code == 200
```

### AAA Pattern (Arrange-Act-Assert)

Every test should follow this pattern:

1. **Arrange**: Set up test data and conditions
2. **Act**: Perform the operation being tested
3. **Assert**: Verify the results

### Example: Testing an API Endpoint

```python
def test_health_endpoint_returns_200(self, client):
    """Health endpoint responds with 200 OK status."""
    # Arrange
    expected_status = 200

    # Act
    response = client.get("/health")

    # Assert
    assert response.status_code == expected_status
```

### Using Fixtures

Fixtures provide reusable test data and setup:

```python
# In conftest.py
@pytest.fixture
def sample_data():
    return {"key": "value"}

# In test file
def test_with_fixture(self, client, sample_data):
    """Test using a fixture."""
    assert sample_data["key"] == "value"
```

### Creating Custom Fixtures

Add to `tests/conftest.py`:

```python
@pytest.fixture
def custom_fixture():
    """Setup and prepare test data."""
    data = {"setup": "complete"}
    yield data
    # Cleanup code here if needed
```

Scope options:
- `scope="function"`: New instance for each test (default)
- `scope="module"`: Shared across all tests in a module
- `scope="session"`: Shared across entire test session

### Async Test Support

For testing async endpoints:

```python
@pytest.mark.asyncio
async def test_async_operation(self):
    """Test async code directly."""
    result = await some_async_function()
    assert result is not None
```

FastAPI's TestClient handles async endpoints automatically, so sync tests work fine:

```python
def test_async_endpoint_via_client(self, client):
    """TestClient handles async endpoints."""
    response = client.get("/async-endpoint")
    assert response.status_code == 200
```

## Running Tests

### Run All Tests

```bash
pytest
```

Shows all test results with summary.

### Run with Verbose Output

```bash
pytest -v
```

Shows individual test names and execution time.

### Run Specific Test File

```bash
pytest tests/test_main.py
```

### Run Specific Test Class

```bash
pytest tests/test_main.py::TestRootEndpoint
```

### Run Specific Test Function

```bash
pytest tests/test_main.py::TestRootEndpoint::test_root_status_code
```

### Run with Keyword Filter

```bash
pytest -k "health"
```

Runs all tests with "health" in their name.

### Run with Multiple Markers

```bash
pytest -m "not slow"
```

Runs tests not marked as slow.

### Run with Output Capture Disabled

```bash
pytest -s
```

Shows print() output from tests (useful for debugging).

### Run Tests and Drop to Debugger on Failure

```bash
pytest --pdb
```

Starts Python debugger when a test fails.

### Run Tests and Show Local Variables on Failure

```bash
pytest -l
```

### Run Tests with Specific Python Version (if multiple installed)

```bash
pytest --co -q  # Collect only
pytest  # Run all
```

## Coverage Requirements

### Understanding Coverage

Coverage measures what percentage of code is executed during tests:

- **Line coverage**: Individual lines of code
- **Branch coverage**: Different code paths (if/else branches)
- **Function coverage**: Whether functions are called

### Minimum Coverage: 70%

- All new code must be tested
- Existing code should have tests
- Enforcement: CI fails if coverage drops below 70%

### Improving Coverage

#### Identify Uncovered Code

```bash
pytest --cov=app --cov-report=term-missing
```

Shows line numbers of all uncovered code.

#### Interactive HTML Report

```bash
pytest --cov=app --cov-report=html
```

Open `htmlcov/index.html` to:
- Click on files to see line-by-line coverage
- Green lines are covered
- Red lines are not covered
- Orange lines have partial coverage (some branches uncovered)

#### Coverage by File

```bash
pytest --cov=app --cov-report=term-missing:skip-covered
```

Shows only files with missing coverage.

### Coverage Exclusions

Some code shouldn't require tests. In `pyproject.toml`:

```toml
[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",    # Add to specific lines
    "def __repr__",        # Debug methods
    "raise NotImplementedError",
    "if TYPE_CHECKING:",   # Type checking imports
]
```

Mark lines to skip coverage:

```python
def debug_only():  # pragma: no cover
    print("Debug info")
```

### Coverage Reports in CI

The CI pipeline:

1. Runs tests with coverage measurement
2. Generates XML report
3. Fails build if coverage < 70%
4. (Optional) Uploads to Codecov for trend tracking

## Best Practices

### 1. One Assertion Per Test (When Possible)

```python
# Good: Each test has one clear purpose
def test_status_code_is_200(self, client):
    assert client.get("/health").status_code == 200

def test_status_value_is_healthy(self, client):
    assert client.get("/health").json()["status"] == "healthy"

# Avoid: Multiple assertions make it unclear what failed
def test_health_endpoint(self, client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    assert "status" in response.json()
```

### 2. Use Descriptive Test Names

Test names should explain what is being tested:

```python
# Good: Clear what's being tested
def test_root_endpoint_returns_version_in_response(self, client):
    ...

# Avoid: Vague names
def test_endpoint(self, client):
    ...
```

### 3. Test Both Success and Failure Cases

```python
def test_valid_input_returns_success(self, client):
    """Test success path."""
    response = client.post("/upload", json={"valid": "data"})
    assert response.status_code == 200

def test_invalid_input_returns_error(self, client):
    """Test failure path."""
    response = client.post("/upload", json={})
    assert response.status_code == 400
```

### 4. Use Fixtures for Shared Data

```python
# Good: Fixtures provide reusable data
@pytest.fixture
def sample_robot_data():
    return {"type": "IRB 4600"}

def test_with_fixture(self, sample_robot_data):
    assert sample_robot_data["type"] == "IRB 4600"

# Avoid: Repeated setup code
def test_without_fixture(self):
    data = {"type": "IRB 4600"}
    assert data["type"] == "IRB 4600"
```

### 5. Keep Tests Fast

- Use fixtures with function scope for isolation
- Mock external dependencies
- Avoid unnecessary computation
- Run fast tests more frequently

### 6. Make Tests Independent

Tests should not depend on each other:

```python
# Good: Each test is independent
def test_first_operation(self, client):
    response = client.post("/action", json={"id": 1})
    assert response.status_code == 200

def test_second_operation(self, client):
    response = client.post("/action", json={"id": 2})
    assert response.status_code == 200

# Avoid: Tests that depend on execution order
def test_operation_creates_data(self, client):
    global test_id
    test_id = 1
    ...

def test_operation_uses_created_data(self, client):
    response = client.post("/action", json={"id": test_id})
    ...
```

### 7. Test at the Appropriate Level

```python
# API tests: Test through HTTP interface
def test_api_endpoint(self, client):
    response = client.get("/health")
    assert response.status_code == 200

# Unit tests: Test individual functions
def test_utility_function():
    result = process_data({"key": "value"})
    assert result == expected

# Integration tests: Test multiple components together
def test_full_workflow(self, client):
    # Upload → Process → Retrieve
    ...
```

### 8. Use Parametrized Tests for Multiple Cases

```python
@pytest.mark.parametrize(
    "endpoint,expected_status",
    [
        ("/", 200),
        ("/health", 200),
        ("/undefined", 404),
    ],
)
def test_endpoint_status_codes(self, client, endpoint, expected_status):
    response = client.get(endpoint)
    assert response.status_code == expected_status
```

## Common Patterns

### Testing API Endpoints

```python
class TestAPIEndpoint:
    """Test pattern for API endpoints."""

    def test_endpoint_status_code(self, client):
        """Test HTTP status code."""
        response = client.get("/endpoint")
        assert response.status_code == 200

    def test_endpoint_response_structure(self, client):
        """Test response has expected fields."""
        response = client.get("/endpoint")
        data = response.json()
        assert "field1" in data
        assert "field2" in data

    def test_endpoint_response_types(self, client):
        """Test response field types are correct."""
        response = client.get("/endpoint")
        data = response.json()
        assert isinstance(data["field1"], str)
        assert isinstance(data["field2"], int)

    def test_endpoint_required_headers(self, client):
        """Test correct headers are present."""
        response = client.get("/endpoint")
        assert response.headers["content-type"] == "application/json"
```

### Testing Error Handling

```python
def test_invalid_request_returns_400(self, client):
    """Test error response for invalid request."""
    response = client.post("/endpoint", json={})
    assert response.status_code == 400

def test_error_response_has_message(self, client):
    """Test error response contains error details."""
    response = client.post("/endpoint", json={})
    data = response.json()
    assert "detail" in data or "error" in data
```

### Testing with Different Input Values

```python
@pytest.mark.parametrize(
    "input_value,expected_result",
    [
        ("valid", True),
        ("", False),
        (None, False),
    ],
)
def test_with_various_inputs(self, input_value, expected_result):
    """Test function with multiple input values."""
    result = validate(input_value)
    assert result == expected_result
```

### Testing Async Functions

```python
@pytest.mark.asyncio
async def test_async_function():
    """Test async function directly."""
    result = await fetch_data()
    assert result is not None
```

### Mocking External Dependencies

```python
from unittest.mock import patch, MagicMock

def test_with_mocked_dependency(self, client):
    """Test with mocked external service."""
    with patch("app.services.external_api") as mock_api:
        mock_api.return_value = {"status": "success"}
        response = client.get("/endpoint")
        assert response.status_code == 200
```

## Troubleshooting

### Tests Not Discovered

**Problem**: `pytest` runs but finds no tests

**Solutions**:
- Ensure test files are named `test_*.py`
- Ensure test classes are named `Test*`
- Ensure test functions are named `test_*`
- Verify `tests/__init__.py` exists
- Run `pytest --collect-only` to see what's discovered

### Import Errors

**Problem**: `ModuleNotFoundError: No module named 'app'`

**Solutions**:
- Ensure you're in the `backend/` directory: `cd backend`
- Ensure backend is installed: `pip install -e .` or add backend to PYTHONPATH
- Check `sys.path` in tests if needed

### Fixture Not Found

**Problem**: `fixture 'client' not found`

**Solutions**:
- Ensure `conftest.py` is in `tests/` directory
- Check fixture name spelling
- Verify conftest.py is in the right directory level

### Coverage Below 70%

**Problem**: Build fails with "coverage below 70%"

**Solutions**:
1. Run coverage report: `pytest --cov=app --cov-report=term-missing`
2. Find uncovered code (marked with line numbers)
3. Write tests for uncovered code
4. Re-run to verify coverage increased

### Async/Await Issues

**Problem**: `RuntimeError: no running event loop`

**Solutions**:
- Use `@pytest.mark.asyncio` for direct async tests
- Use `TestClient` for FastAPI endpoints (handles async automatically)
- Ensure pytest-asyncio is installed

### TestClient Issues

**Problem**: `TestClient` not working correctly

**Solutions**:
- Import from `fastapi.testclient`: `from fastapi.testclient import TestClient`
- Don't run TestClient in async context (use sync tests)
- Ensure app is imported correctly

## Advanced Topics

### Pytest Plugins

Useful plugins for enhanced testing:

```bash
pip install pytest-cov        # Coverage reporting
pip install pytest-asyncio    # Async test support
pip install pytest-mock       # Mocking utilities
pip install pytest-timeout    # Timeout handling
```

### Pytest Markers

Create custom test markers:

```python
import pytest

@pytest.mark.slow
def test_slow_operation():
    ...

@pytest.mark.integration
def test_api_integration():
    ...
```

Run specific markers:

```bash
pytest -m "not slow"      # Run all except slow tests
pytest -m "integration"   # Run only integration tests
```

### Pytest Hooks and Configuration

Advanced configuration in `pyproject.toml`:

```toml
[tool.pytest.ini_options]
markers = [
    "slow: marks tests as slow",
    "integration: marks tests as integration tests",
]
```

### Database Testing

For future tests with a database:

```python
@pytest.fixture
def db_session():
    """Setup test database."""
    db = TestingSessionLocal()
    yield db
    db.close()
```

### Performance Testing

Using pytest-benchmark (install separately):

```bash
pip install pytest-benchmark
```

```python
def test_endpoint_performance(self, client, benchmark):
    """Benchmark endpoint performance."""
    result = benchmark(client.get, "/health")
    assert result.status_code == 200
```

## Checklist for New Tests

When writing new tests, use this checklist:

- [ ] Test file is named `test_*.py`
- [ ] Test class is named `Test*`
- [ ] Test functions are named `test_*`
- [ ] Tests use descriptive names (clear purpose)
- [ ] Tests follow AAA pattern (Arrange-Act-Assert)
- [ ] Tests use appropriate fixtures
- [ ] Success cases are tested
- [ ] Error/failure cases are tested
- [ ] Tests are independent (no order dependency)
- [ ] Tests are fast (< 1 second each if possible)
- [ ] Response structure is validated
- [ ] Response types are validated
- [ ] Response values are validated
- [ ] HTTP status codes are verified
- [ ] Headers are checked if relevant
- [ ] Edge cases are considered
- [ ] Tests have clear docstrings
- [ ] Tests don't have side effects
- [ ] Coverage is measured: `pytest --cov=app`
- [ ] Coverage is >= 70%
- [ ] All tests pass: `pytest -v`
- [ ] Code passes linting: `ruff check .`

## Resources

- **pytest Documentation**: https://docs.pytest.org/
- **FastAPI Testing**: https://fastapi.tiangolo.com/advanced/testing-dependencies/
- **Python unittest Documentation**: https://docs.python.org/3/library/unittest.html
- **Pytest Fixtures**: https://docs.pytest.org/en/stable/fixtures.html
- **Coverage.py**: https://coverage.readthedocs.io/

## Project-Specific Resources

- **Backend Setup**: See `docs/guides/setup.md`
- **Development Commands**: See `CLAUDE.md` - Backend section
- **Architecture**: See `docs/architecture/`
- **Roadmap**: See `docs/roadmap/11-week-plan.md`

---

**Last Updated**: Week 1 of Development
**Maintainer**: SAIT Research Team
**Status**: Active
