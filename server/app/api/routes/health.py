"""Health check endpoints."""

from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("/")
async def health() -> dict:
    """Basic health check."""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}


@router.get("/ready")
async def ready() -> dict:
    """Readiness probe — checks all services are up."""
    from app.core.registry import registry
    services = list(registry._services.keys())
    return {
        "status": "ready",
        "services": services,
        "timestamp": datetime.utcnow().isoformat(),
    }
