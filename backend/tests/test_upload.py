"""
Test upload endpoints
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app
from pathlib import Path

client = TestClient(app)

# Get fixtures directory
FIXTURES_DIR = Path(__file__).parent / "fixtures" / "rapid"


def test_upload_rapid_valid_file():
    """Test uploading valid RAPID file"""
    # Read sample RAPID file
    rapid_file = FIXTURES_DIR / "simple_movel.mod"
    with open(rapid_file, "rb") as f:
        files = {"file": ("simple_movel.mod", f, "text/plain")}
        response = client.post("/api/upload/rapid", files=files)

    assert response.status_code == 200
    data = response.json()

    # Check response structure
    assert data["filename"] == "simple_movel.mod"
    assert "file_id" in data
    assert data["file_id"].startswith("rapid_")
    assert isinstance(data["ast"], list)
    assert isinstance(data["errors"], list)
    assert isinstance(data["warnings"], list)


def test_upload_rapid_invalid_extension():
    """Test uploading file with wrong extension"""
    files = {"file": ("test.txt", b"some content", "text/plain")}
    response = client.post("/api/upload/rapid", files=files)

    assert response.status_code == 400
    assert "Only .mod files accepted" in response.json()["detail"]


def test_upload_rapid_file_too_large():
    """Test uploading file that exceeds size limit"""
    # Create >1MB file
    large_content = b"A" * (1_000_001)
    files = {"file": ("large.mod", large_content, "text/plain")}
    response = client.post("/api/upload/rapid", files=files)

    assert response.status_code == 400
    assert "File too large" in response.json()["detail"]


def test_upload_rapid_binary_file():
    """Test uploading binary file (should fail validation)"""
    # Binary content that's not valid UTF-8
    binary_content = bytes([0xFF, 0xFE, 0xFD, 0xFC] * 100)
    files = {"file": ("binary.mod", binary_content, "application/octet-stream")}
    response = client.post("/api/upload/rapid", files=files)

    assert response.status_code == 400
    assert "must be valid text" in response.json()["detail"]


def test_upload_obstacle_valid_stl():
    """Test uploading valid STL file"""
    # Minimal ASCII STL content
    stl_content = b"""solid test
facet normal 0 0 1
  outer loop
    vertex 0 0 0
    vertex 1 0 0
    vertex 0 1 0
  endloop
endfacet
endsolid test
"""
    files = {"file": ("cube.stl", stl_content, "application/octet-stream")}
    response = client.post("/api/upload/obstacle", files=files)

    assert response.status_code == 200
    data = response.json()

    # Check response structure
    assert data["filename"] == "cube.stl"
    assert "obstacle_id" in data
    assert data["obstacle_id"].startswith("obs_")
    assert data["position"] == [0.0, 0.0, 0.0]  # Default position
    assert data["rotation"] == [0.0, 0.0, 0.0]  # Default rotation
    assert "bounds" in data
    assert "vertices" in data
    assert "triangles" in data


def test_upload_obstacle_with_transform():
    """Test uploading obstacle with position and rotation"""
    stl_content = b"solid test\nendsolid test"
    files = {"file": ("test.stl", stl_content, "application/octet-stream")}
    data = {
        "position": "[500, 100, 0]",
        "rotation": "[0, 0, 45]"
    }
    response = client.post("/api/upload/obstacle", files=files, data=data)

    assert response.status_code == 200
    result = response.json()
    assert result["position"] == [500, 100, 0]
    assert result["rotation"] == [0, 0, 45]


def test_upload_obstacle_invalid_extension():
    """Test uploading file with wrong extension"""
    files = {"file": ("test.obj", b"some content", "application/octet-stream")}
    response = client.post("/api/upload/obstacle", files=files)

    assert response.status_code == 400
    assert "Only .stl files accepted" in response.json()["detail"]


def test_upload_obstacle_file_too_large():
    """Test uploading obstacle file that exceeds 10MB limit"""
    large_content = b"solid test\n" + b"A" * 10_000_001
    files = {"file": ("huge.stl", large_content, "application/octet-stream")}
    response = client.post("/api/upload/obstacle", files=files)

    assert response.status_code == 400
    assert "File too large" in response.json()["detail"]


def test_upload_obstacle_invalid_position():
    """Test uploading obstacle with invalid position format"""
    stl_content = b"solid test\nendsolid test"
    files = {"file": ("test.stl", stl_content, "application/octet-stream")}
    data = {"position": "[500, 100]"}  # Invalid: only 2 values instead of 3
    response = client.post("/api/upload/obstacle", files=files, data=data)

    assert response.status_code == 400
    assert "Invalid position or rotation format" in response.json()["detail"]


def test_upload_obstacle_empty_file():
    """Test uploading empty STL file"""
    files = {"file": ("empty.stl", b"", "application/octet-stream")}
    response = client.post("/api/upload/obstacle", files=files)

    assert response.status_code == 400
    assert "Invalid STL file format" in response.json()["detail"]
