"""Robot status and control REST endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Depends

from app.api.dependencies.get_services import get_robot_controller, get_ws_manager

router = APIRouter(prefix="/robot", tags=["Robot"])


@router.get("/state")
async def get_state(
    controller=Depends(get_robot_controller),
) -> dict:
    """Get the current robot state."""
    return {
        "state": controller.current_state,
        "is_awake": controller.is_awake,
    }


@router.get("/connections")
async def get_connections(
    ws_manager=Depends(get_ws_manager),
) -> dict:
    """Get active WebSocket connection count."""
    return {
        "active_connections": ws_manager.connection_count,
        "session_ids": list(ws_manager.session_ids),
    }
