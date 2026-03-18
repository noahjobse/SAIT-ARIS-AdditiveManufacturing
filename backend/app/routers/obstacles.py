"""
GET /api/obstacles — list all obstacles
DELETE /api/obstacles/{obstacle_id} — remove an obstacle
"""
import logging

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.obstacles.registry import obstacle_registry

router = APIRouter()
logger = logging.getLogger(__name__)


class ObstacleListItem(BaseModel):
    obstacle_id: str
    filename: str
    position: list[float]
    rotation: list[float]
    created_at: str


@router.get("/api/obstacles", response_model=list[ObstacleListItem])
async def list_obstacles():
    """List all registered obstacles."""
    return [
        ObstacleListItem(
            obstacle_id=r.obstacle_id,
            filename=r.filename,
            position=r.position,
            rotation=r.rotation,
            created_at=r.created_at,
        )
        for r in obstacle_registry.list_all()
    ]


@router.delete("/api/obstacles/{obstacle_id}", status_code=204)
async def delete_obstacle(obstacle_id: str):
    """Delete an obstacle by ID."""
    deleted = obstacle_registry.delete(obstacle_id)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Obstacle '{obstacle_id}' not found")
