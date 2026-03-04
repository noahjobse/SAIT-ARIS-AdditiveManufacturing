"""
Response schemas for API endpoints
"""

from pydantic import BaseModel


class ErrorDetail(BaseModel):
    """Error or warning detail"""
    line: int
    message: str


class RapidUploadResponse(BaseModel):
    """Response from RAPID file upload"""
    filename: str
    file_id: str
    ast: list[dict]  # AST nodes (will be populated by parser in Week 3-4)
    errors: list[ErrorDetail]
    warnings: list[ErrorDetail]


class BoundingBox(BaseModel):
    """3D bounding box"""
    min: list[float]  # [x, y, z]
    max: list[float]  # [x, y, z]


class ObstacleUploadResponse(BaseModel):
    """Response from obstacle STL upload"""
    obstacle_id: str
    filename: str
    position: list[float]  # [x, y, z] in mm
    rotation: list[float]  # [rx, ry, rz] in degrees
    bounds: BoundingBox
    vertices: int
    triangles: int
