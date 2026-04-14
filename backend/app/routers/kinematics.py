"""API endpoints for robot kinematics (FK/IK)."""
import asyncio
import functools
import logging
import threading

from fastapi import APIRouter, HTTPException, status

from app.kinematics.exceptions import (
    IKSolutionNotFoundError,
    InvalidJointAnglesError,
    RobotNotLoadedError,
)
from app.kinematics.solver import KinematicsSolver
from app.schemas.kinematics import FKRequest, FKResponse, IKRequest, IKResponse
from app.thread_pool import executor, pybullet_lock

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/kinematics", tags=["kinematics"])

# Global solver instance (reused across requests)
_solver: KinematicsSolver = None
_solver_lock = threading.Lock()


def get_solver() -> KinematicsSolver:
    """Get or create global kinematics solver instance (double-checked locking)."""
    global _solver
    if _solver is None:
        with _solver_lock:
            if _solver is None:
                _solver = KinematicsSolver(headless=True)
    return _solver


# ---------------------------------------------------------------------------
# Sync helpers (run in thread pool)
# ---------------------------------------------------------------------------

def _run_fk_sync(robot_id: str, joint_angles: list) -> dict:
    """Call forward_kinematics in a thread — raises on error."""
    return get_solver().forward_kinematics(robot_id, joint_angles)


def _run_ik_sync(
    robot_id: str,
    target_position: list,
    target_orientation: list | None,
    current_joints: list | None,
) -> dict:
    """Call inverse_kinematics in a thread — raises on error."""
    return get_solver().inverse_kinematics(
        robot_id, target_position, target_orientation, current_joints
    )


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.post("/fk", response_model=FKResponse, status_code=status.HTTP_200_OK)
async def forward_kinematics(request: FKRequest):
    """
    Calculate end-effector pose from joint angles (Forward Kinematics).

    Args:
        request: FK request with robot_id and joint_angles

    Returns:
        FKResponse with position and orientation
    """
    loop = asyncio.get_event_loop()
    try:
        async with pybullet_lock:
            result = await loop.run_in_executor(
                executor, functools.partial(_run_fk_sync, request.robot_id, request.joint_angles)
            )
    except InvalidJointAnglesError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid joint angles: {str(e)}",
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except RobotNotLoadedError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except FileNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Robot URDF not found: {str(e)}",
        )
    except Exception as e:
        logger.error(f"FK error: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Forward kinematics failed: {str(e)}",
        )

    return FKResponse(
        robot_id=request.robot_id,
        position=result["position"],
        orientation=result["orientation"],
    )


@router.post("/ik", response_model=IKResponse, status_code=status.HTTP_200_OK)
async def inverse_kinematics(request: IKRequest):
    """
    Calculate joint angles to reach target pose (Inverse Kinematics).

    Args:
        request: IK request with robot_id, target_position, and optional orientation

    Returns:
        IKResponse with calculated joint_angles
    """
    loop = asyncio.get_event_loop()
    try:
        async with pybullet_lock:
            result = await loop.run_in_executor(
                executor,
                functools.partial(
                    _run_ik_sync,
                    request.robot_id,
                    request.target_position,
                    request.target_orientation,
                    request.current_joints,
                ),
            )
    except IKSolutionNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except RobotNotLoadedError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except FileNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Robot URDF not found: {str(e)}",
        )
    except Exception as e:
        logger.error(f"IK error: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Inverse kinematics failed: {str(e)}",
        )

    return IKResponse(
        robot_id=request.robot_id,
        joint_angles=result["joint_angles"],
    )
