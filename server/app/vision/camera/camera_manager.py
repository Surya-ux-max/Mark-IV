"""Virtual camera manager stub.

In virtual mode, vision events are injected via WebSocket from the client.
Real camera integration (OpenCV) plugs in here by implementing the same interface.
"""

from __future__ import annotations

from app.core.logging import get_logger

logger = get_logger(__name__)


class VirtualCameraManager:
    """Virtual camera — no real frames. Events come from WebSocket client."""

    async def start(self) -> None:
        logger.info("camera_virtual_mode_active")

    async def stop(self) -> None:
        pass

    async def get_frame(self) -> None:
        """Virtual mode — no frames."""
        return None
