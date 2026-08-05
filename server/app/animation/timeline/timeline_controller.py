"""Timeline controller — main orchestrator for all animations.

Receives ANIMATION_REQUESTED events from all subsystems,
enqueues frames, and broadcasts them to the frontend via WSManager.

Supports:
  - Parallel animations (face + hands + legs simultaneously)
  - Priority-based preemption
  - Smooth transitions via transition_ms in expressions
"""

from __future__ import annotations

from typing import Any

from app.animation.timeline.animation_frame import AnimationFrame
from app.animation.timeline.animation_queue import AnimationQueue
from app.core.logging import get_logger

logger = get_logger(__name__)


class TimelineController:
    """Orchestrates multi-track animation playback."""

    def __init__(self) -> None:
        self._queue = AnimationQueue()
        self._broadcast_fn = None   # injected: async (payload: dict) -> None

    def set_broadcast(self, fn) -> None:
        """Inject the WSManager broadcast function."""
        self._broadcast_fn = fn

    async def on_animation_requested(self, event_type: str, payload: Any) -> None:
        """Handle ANIMATION_REQUESTED event — enqueue and broadcast."""
        frame = AnimationFrame(
            animation=payload.get("animation", "UNKNOWN"),
            target=payload.get("target", "body"),
            params=payload.get("params", {}),
            duration_ms=payload.get("total_duration_ms", payload.get("duration_ms", 1000)),
            priority=payload.get("priority", 5),
            interruptible=payload.get("interruptible", True),
            parallel=payload.get("parallel", True),
            loop=payload.get("loop", False),
            frames=payload.get("frames", []),
        )
        await self._queue.enqueue(frame)

        # Broadcast immediately to all WebSocket clients
        if self._broadcast_fn:
            try:
                await self._broadcast_fn({"type": "ANIMATION_CUE", **frame.to_ws_payload()})
            except Exception as exc:
                logger.warning("timeline_broadcast_failed", error=str(exc))

        logger.debug(
            "animation_queued",
            animation=frame.animation,
            target=frame.target,
            duration_ms=frame.duration_ms,
        )

    async def on_expression_changed(self, event_type: str, payload: Any) -> None:
        """Handle EXPRESSION_CHANGED — broadcast as face animation cue."""
        if self._broadcast_fn:
            await self._broadcast_fn({
                "type": "EXPRESSION_CHANGED",
                **payload,
            })

    async def on_gesture_started(self, event_type: str, payload: Any) -> None:
        logger.debug("gesture_started_timeline", gesture=payload.get("gesture"))

    async def on_animation_completed(self, event_type: str, payload: Any) -> None:
        target = payload.get("target", "unknown")
        self._queue.clear_target(target)
