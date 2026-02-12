"""
Request schemas for API endpoints
"""
from pydantic import BaseModel
from typing import List, Dict, Optional


class SimulateRequest(BaseModel):
    """Request for simulation (Week 5-6 implementation)"""
    robot_id: str
    ast: List[Dict]  # Parsed AST from RAPID upload
    obstacles: List[Dict]  # List of obstacle IDs with transforms
