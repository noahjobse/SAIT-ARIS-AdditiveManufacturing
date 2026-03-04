"""
Robot model endpoints
"""
from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

router = APIRouter()

# Path to robot models (relative to project root)
MODELS_DIR = Path(__file__).parent.parent.parent.parent / "frontend" / "public" / "models" / "robots"


@router.get("/api/robots/{robot_id}/model")
async def get_robot_model(robot_id: str):
    """
    Get robot 3D model (GLB format)

    Args:
        robot_id: Robot identifier (irb4600, irb2600, irb6700)

    Returns:
        Binary GLB file for Babylon.js rendering

    Raises:
        HTTPException: If robot ID is invalid or model file not found
    """
    # Validate robot ID
    valid_robots = ["irb4600", "irb2600", "irb6700"]
    if robot_id not in valid_robots:
        raise HTTPException(
            status_code=404,
            detail=f"Invalid robot ID. Must be one of: {', '.join(valid_robots)}"
        )

    # Map robot IDs to GLB files
    # For now, only IRB 4600 has a GLB file
    model_files = {
        "irb4600": "irb4600/Model_IRB_4600.glb",
        "irb2600": "irb2600/Model_IRB_2600.glb",
        "irb6700": "irb6700/Model_IRB_6700.glb"
    }

    model_path = MODELS_DIR / model_files[robot_id]

    # Check if file exists
    if not model_path.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Model file not found for {robot_id}. File may not be available yet."
        )

    # Return GLB file as binary
    return FileResponse(
        path=str(model_path),
        media_type="application/octet-stream",
        filename=f"{robot_id}.glb"
    )
