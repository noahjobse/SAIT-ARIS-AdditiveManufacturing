"""
Request schemas for API endpoints
"""

from pydantic import BaseModel


class SimulateRequest(BaseModel):
    """Request for simulation (Week 5-6 implementation)"""
    robot_id: str
    ast: list[dict]  # Parsed AST from RAPID upload
    obstacles: list[dict]  # List of obstacle IDs with transforms
