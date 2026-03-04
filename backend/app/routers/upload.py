"""
Upload endpoints for RAPID programs and obstacles
"""
import json

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from app.schemas.responses import BoundingBox, ObstacleUploadResponse, RapidUploadResponse
from app.utils.file_handler import (
    generate_file_id,
    save_temp_file,
    validate_rapid_file,
    validate_stl_file,
)

router = APIRouter()


@router.post("/api/upload/rapid", response_model=RapidUploadResponse)
async def upload_rapid(file: UploadFile = File(...)):
    """
    Upload RAPID program file (.mod)

    Args:
        file: RAPID source file (.mod extension, max 1MB)

    Returns:
        Parsed AST (placeholder for now - parser will be implemented in Week 3-4)

    Raises:
        HTTPException: If file is invalid, too large, or wrong type
    """
    # Validate file extension
    if not file.filename.endswith(".mod"):
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Only .mod files accepted."
        )

    # Read file contents
    contents = await file.read()

    # Check file size (max 1MB)
    if len(contents) > 1_000_000:  # 1MB
        raise HTTPException(
            status_code=400,
            detail="File too large. Maximum 1MB allowed."
        )

    # Validate file is text (not binary)
    if not validate_rapid_file(contents):
        raise HTTPException(
            status_code=400,
            detail="Invalid RAPID file. File must be valid text."
        )

    # Generate unique file ID
    file_id = generate_file_id("rapid")

    # Save to temp location
    save_temp_file(file_id, contents, ".mod")

    # Placeholder AST - real parser will populate this in Week 3-4
    # For now, just return empty AST with no errors
    return RapidUploadResponse(
        filename=file.filename,
        file_id=file_id,
        ast=[],  # Parser will populate this
        errors=[],
        warnings=[]
    )


@router.post("/api/upload/obstacle", response_model=ObstacleUploadResponse)
async def upload_obstacle(
    file: UploadFile = File(...),
    position: str | None = Form(None),
    rotation: str | None = Form(None)
):
    """
    Upload obstacle STL file

    Args:
        file: STL mesh file (.stl extension, max 10MB)
        position: Optional JSON string "[x, y, z]" in mm (default: [0, 0, 0])
        rotation: Optional JSON string "[rx, ry, rz]" in degrees (default: [0, 0, 0])

    Returns:
        Obstacle metadata including ID, bounds, and transform

    Raises:
        HTTPException: If file is invalid, too large, or wrong type
    """
    # Validate file extension
    if not file.filename.endswith(".stl"):
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Only .stl files accepted."
        )

    # Read file contents
    contents = await file.read()

    # Check file size (max 10MB)
    if len(contents) > 10_000_000:  # 10MB
        raise HTTPException(
            status_code=400,
            detail="File too large. Maximum 10MB allowed."
        )

    # Validate STL format
    if not validate_stl_file(contents):
        raise HTTPException(
            status_code=400,
            detail="Invalid STL file format."
        )

    # Generate unique obstacle ID
    obstacle_id = generate_file_id("obs")

    # Save file
    save_temp_file(obstacle_id, contents, ".stl")

    # Parse position/rotation (default to origin)
    try:
        pos = json.loads(position) if position else [0.0, 0.0, 0.0]
        rot = json.loads(rotation) if rotation else [0.0, 0.0, 0.0]

        # Validate position/rotation format
        if not (isinstance(pos, list) and len(pos) == 3):
            raise ValueError("Position must be [x, y, z]")
        if not (isinstance(rot, list) and len(rot) == 3):
            raise ValueError("Rotation must be [rx, ry, rz]")

    except (json.JSONDecodeError, ValueError) as e:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid position or rotation format: {str(e)}"
        )

    # Placeholder bounds - real mesh analysis will compute this in Week 5-6
    # For now, just return a dummy bounding box
    return ObstacleUploadResponse(
        obstacle_id=obstacle_id,
        filename=file.filename,
        position=pos,
        rotation=rot,
        bounds=BoundingBox(
            min=[0.0, 0.0, 0.0],  # Will be computed from actual STL
            max=[100.0, 100.0, 100.0]  # Placeholder
        ),
        vertices=0,  # Will be computed from STL
        triangles=0  # Will be computed from STL
    )
