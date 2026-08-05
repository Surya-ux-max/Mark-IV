"""Leg controller — orchestrates leg/movement animations via event bus.

Hardware swap: replace event_bus.publish with servo command calls.
"""

from __future__ import annotations

import asyncio
from typing import List, Optional

from app.animation.legs.leg_pose import LegPose
from app.animation.legs.movement_library import MovementLibrary
from app.core.logging import get_logger
from app.events.event_bus import event_bus
from app.events.event_types import EventType

logger = get_logger(__name__)


class LegController:
    """Controls leg animations via the event bus."""

    def __init__(self) -> None:
        self._moving = False
        self._lock = asyncio.Lock()

    async def play(self, movement_name: str) -> None:
        async with self._lock:
            frames = MovementLibrary.get(movement_name)
            if not frames:
                logger.warning("movement_not_found", movement=movement_name)
                return
            self._moving = True
            total_ms = sum(f.duration_ms for f in frames)
            await event_bus.publish(
                EventType.ANIMATION_REQUESTED,
                {
                    "animation": f"LEG_{movement_name.upper()}",
                    "target": "legs",
                    "frames": [self._frame_to_dict(f) for f in frames],
                    "total_duration_ms": total_ms,
                },
            )
            asyncio.create_task(self._finish_after(total_ms / 1000))

    async def _finish_after(self, delay: float) -> None:
        await asyncio.sleep(delay)
        self._moving = False
        await event_bus.publish(EventType.ANIMATION_COMPLETED, {"target": "legs"})

    @staticmethod
    def _frame_to_dict(pose: LegPose) -> dict:
        return {
            "left_hip_angle":   pose.left_hip_angle,
            "right_hip_angle":  pose.right_hip_angle,
            "left_knee_angle":  pose.left_knee_angle,
            "right_knee_angle": pose.right_knee_angle,
            "body_lean":        pose.body_lean,
            "duration_ms":      pose.duration_ms,
        }

    # ── Convenience shortcuts ──────────────────────────────────────────────────
    async def walk(self) -> None:         await self.play("walk")
    async def turn_left(self) -> None:    await self.play("turn_left")
    async def turn_right(self) -> None:   await self.play("turn_right")
    async def idle_stance(self) -> None:  await self.play("idle_sway")
    async def idle_bounce(self) -> None:  await self.play("idle_bounce")

    @property
    def is_moving(self) -> bool:
        return self._moving
