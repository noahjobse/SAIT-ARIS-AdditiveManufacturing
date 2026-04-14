"""
POST /api/print/upload  — accept and validate STL file
POST /api/print/slice   — slice STL → RAPID AST → IK trajectory with extrusion data
"""
import asyncio
import functools
import logging
import math
import os
import tempfile
import threading
import time
import uuid

from fastapi import APIRouter, File, HTTPException, UploadFile
from pydantic import BaseModel

from app.kinematics.solver import KinematicsSolver
from app.printing.slicer import SliceResult, slice_stl
from app.schemas.simulate import (
    SimulationStats,
    TCPPose,
    TrajectoryWaypoint,
)
from app.thread_pool import executor, pybullet_lock
from app.trajectory.generator import TrajectoryError, TrajectoryGenerator

router = APIRouter()
logger = logging.getLogger(__name__)

_solver = KinematicsSolver()
_generator = TrajectoryGenerator(_solver)

# In-memory store: file_id → temp path
_uploads: dict[str, str] = {}
_uploads_lock = threading.Lock()

MAX_STL_SIZE = 50 * 1024 * 1024  # 50 MB


# ---------------------------------------------------------------------------
# Request / Response schemas
# ---------------------------------------------------------------------------

class SliceRequest(BaseModel):
    file_id: str
    robot_id: str = "irb4600"
    layer_height: float = 0.2
    nozzle_diameter: float = 0.4


class PrintStats(BaseModel):
    layer_count: int
    total_extrusion_mm: float
    move_commands: int
    print_height_mm: float
    slice_time_ms: float


class PrintSimulateResponse(BaseModel):
    trajectory: list[TrajectoryWaypoint]
    stats: SimulationStats
    print_stats: PrintStats


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.post("/api/print/upload")
async def upload_stl(file: UploadFile = File(...)):
    """Upload and validate an STL file for slicing."""
    if not file.filename or not file.filename.lower().endswith(".stl"):
        raise HTTPException(400, "Only .stl files are accepted")

    content = await file.read()
    if len(content) > MAX_STL_SIZE:
        raise HTTPException(
            400,
            f"File too large ({len(content) // 1024}KB). Maximum: {MAX_STL_SIZE // (1024 * 1024)}MB",
        )

    file_id = uuid.uuid4().hex[:12]
    tmp_dir = tempfile.mkdtemp(prefix="armstudio_stl_")
    tmp_path = os.path.join(tmp_dir, f"{file_id}.stl")

    with open(tmp_path, "wb") as f:
        f.write(content)

    with _uploads_lock:
        _uploads[file_id] = tmp_path
    logger.info("Stored STL upload %s (%d bytes) at %s", file_id, len(content), tmp_path)

    return {"file_id": file_id, "filename": file.filename, "size_bytes": len(content)}


# ---------------------------------------------------------------------------
# Sync helper (runs in thread pool)
# ---------------------------------------------------------------------------

def _run_slice_sync(request: SliceRequest, stl_path: str) -> PrintSimulateResponse:
    """
    CPU-bound slice + IK work — executed in a thread pool via run_in_executor.

    Raises HTTPException for known error cases so the executor propagates it.
    """
    # ── Step 1: Slice STL into move commands ──
    slice_start = time.monotonic()
    try:
        result: SliceResult = slice_stl(
            stl_path,
            layer_height=request.layer_height,
            nozzle_diameter=request.nozzle_diameter,
        )
    except ValueError as e:
        raise HTTPException(400, str(e))
    except Exception as e:
        logger.exception("Slicing failed")
        raise HTTPException(500, f"Slicing failed: {e}")

    slice_ms = (time.monotonic() - slice_start) * 1000

    # ── Step 2: Generate IK trajectory ──
    sim_start = time.monotonic()
    deadline = time.monotonic() + 30.0

    try:
        raw_waypoints, timed_out = _generator.generate(
            result.program, request.robot_id, deadline=deadline
        )
    except TrajectoryError as e:
        raise HTTPException(400, f"Trajectory generation failed: {e}")
    except Exception as e:
        logger.exception("Trajectory generation failed")
        raise HTTPException(500, f"Trajectory generation failed: {e}")

    sim_ms = (time.monotonic() - sim_start) * 1000

    if not raw_waypoints:
        raise HTTPException(400, "Trajectory generation produced no waypoints")

    # ── Step 3: Annotate waypoints with interpolated extrusion ──
    _interpolate_extrusion(raw_waypoints, result.extrusion_values)

    # ── Step 4: Build response ──
    MM_PER_M = 1000.0
    waypoints: list[TrajectoryWaypoint] = []

    for i, wp in enumerate(raw_waypoints):
        joints_deg = [math.degrees(j) for j in wp["joints"]]
        pos_mm = [c * MM_PER_M for c in wp["position"]]

        waypoints.append(
            TrajectoryWaypoint(
                index=i,
                timestamp=wp["timestamp"],
                joints=joints_deg,
                tcp_pose=TCPPose(position=pos_mm, orientation=[1.0, 0.0, 0.0, 0.0]),
                collisions=[],
                extrusion=wp.get("_extrusion"),
            )
        )

    duration = raw_waypoints[-1]["timestamp"]
    total_ms = slice_ms + sim_ms

    return PrintSimulateResponse(
        trajectory=waypoints,
        stats=SimulationStats(
            total_waypoints=len(waypoints),
            duration_seconds=round(duration, 3),
            collisions_detected=0,
            ik_failures=0,
            computation_time_ms=round(total_ms, 1),
            timed_out=timed_out,
        ),
        print_stats=PrintStats(
            layer_count=result.stats["layer_count"],
            total_extrusion_mm=result.stats["total_extrusion_mm"],
            move_commands=result.stats["move_commands"],
            print_height_mm=result.stats["print_height_mm"],
            slice_time_ms=round(slice_ms, 1),
        ),
    )


@router.post("/api/print/slice", response_model=PrintSimulateResponse)
async def slice_and_simulate(request: SliceRequest):
    """Full pipeline: STL → trimesh slice → RAPID AST → IK trajectory."""
    if request.robot_id not in ("irb4600", "irb2600", "irb6700"):
        raise HTTPException(400, f"Unknown robot_id: {request.robot_id!r}")

    with _uploads_lock:
        stl_path = _uploads.get(request.file_id)
    if not stl_path or not os.path.exists(stl_path):
        raise HTTPException(404, f"STL file not found for file_id: {request.file_id}")

    loop = asyncio.get_event_loop()
    async with pybullet_lock:
        try:
            result = await loop.run_in_executor(
                executor, functools.partial(_run_slice_sync, request, stl_path)
            )
        except HTTPException:
            raise
        except Exception as e:
            logger.exception("Unexpected error during slice and simulate")
            raise HTTPException(500, f"Slice and simulate failed: {e}")
    return result


def _interpolate_extrusion(
    waypoints: list[dict], extrusion_values: list[float]
) -> None:
    """Annotate each waypoint with linearly interpolated cumulative extrusion.

    Waypoints within a command are assigned E values interpolated between
    the previous command's E (start) and this command's E (end).
    Travel commands (where E doesn't change) get None.
    """
    if not extrusion_values:
        return

    # Group waypoints by command_index
    groups: dict[int, list[int]] = {}
    for wp_idx, wp in enumerate(waypoints):
        ci = wp.get("command_index", 0)
        groups.setdefault(ci, []).append(wp_idx)

    for ci, wp_indices in groups.items():
        e_start = extrusion_values[ci - 1] if ci > 0 else 0.0
        e_end = extrusion_values[ci] if ci < len(extrusion_values) else e_start

        if abs(e_end - e_start) < 1e-6:
            # No extrusion change → travel move
            for wp_idx in wp_indices:
                waypoints[wp_idx]["_extrusion"] = None
        else:
            # Linearly interpolate E across waypoints in this command
            n = len(wp_indices)
            for j, wp_idx in enumerate(wp_indices):
                alpha = (j + 1) / n
                waypoints[wp_idx]["_extrusion"] = e_start + alpha * (e_end - e_start)
