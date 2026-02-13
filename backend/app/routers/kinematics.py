"""API endpoints for robot kinematics (FK/IK)."""
import logging
from fastapi import APIRouter, HTTPException, status

from app.schemas.kinematics import FKRequest, FKResponse, IKRequest, IKResponse
from app.kinematics.solver import KinematicsSolver
from app.kinematics.exceptions import (
    IKSolutionNotFoundError,
    InvalidJointAnglesError,
    RobotNotLoadedError,
)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/kinematics", tags=["kinematics"])

# Global solver instance (reused across requests)
_solver: KinematicsSolver = None


def get_solver() -> KinematicsSolver:
    """Get or create global kinematics solver instance."""
    global _solver
    if _solver is None:
        _solver = KinematicsSolver(headless=True)
    return _solver


@router.post("/fk", response_model=FKResponse, status_code=status.HTTP_200_OK)
async def forward_kinematics(request: FKRequest):
    """
    Calculate end-effector pose from joint angles (Forward Kinematics).

    Args:
        request: FK request with robot_id and joint_angles

    Returns:
        FKResponse with position and orientation
    """
    try:
        solver = get_solver()
        result = solver.forward_kinematics(request.robot_id, request.joint_angles)

        return FKResponse(
            robot_id=request.robot_id,
            position=result["position"],
            orientation=result["orientation"],
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


@router.post("/ik", response_model=IKResponse, status_code=status.HTTP_200_OK)
async def inverse_kinematics(request: IKRequest):
    """
    Calculate joint angles to reach target pose (Inverse Kinematics).

    Args:
        request: IK request with robot_id, target_position, and optional orientation

    Returns:
        IKResponse with calculated joint_angles
    """
    try:
        solver = get_solver()
        result = solver.inverse_kinematics(
            request.robot_id,
            request.target_position,
            request.target_orientation,
            request.current_joints,
        )

        return IKResponse(
            robot_id=request.robot_id,
            joint_angles=result["joint_angles"],
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
