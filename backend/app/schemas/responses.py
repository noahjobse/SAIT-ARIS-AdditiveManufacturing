"""
Response schemas for API endpoints
"""
from pydantic import BaseModel
from typing import List, Dict, Optional


class ErrorDetail(BaseModel):
    """Error or warning detail"""
    line: int
    message: str


class RapidUploadResponse(BaseModel):
    """Response from RAPID file upload"""
    filename: str
    file_id: str
    ast: List[Dict]  # AST nodes (will be populated by parser in Week 3-4)
    errors: List[ErrorDetail]
    warnings: List[ErrorDetail]


class BoundingBox(BaseModel):
    """3D bounding box"""
    min: List[float]  # [x, y, z]
    max: List[float]  # [x, y, z]


class ObstacleUploadResponse(BaseModel):
    """Response from obstacle STL upload"""
    obstacle_id: str
    filename: str
    position: List[float]  # [x, y, z] in mm
    rotation: List[float]  # [rx, ry, rz] in degrees
    bounds: BoundingBox
    vertices: int
    triangles: int
