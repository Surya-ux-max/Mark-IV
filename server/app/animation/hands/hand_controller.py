"""Hand controller — orchestrates gesture playback and event publishing.

This is the primary entry point for triggering hand animations.
In virtual mode: publishes animation events to the event bus.
In hardware mode: sends servo commands to the arm controller.
"""

from __future__ import annotations

import asyncio
from typing import Any, List, Optional

from app.animation.hands.gesture_library import GestureLibrary
from app.animation.hands.pose import HandPose
from app.core.logging import get_logger
from app.events.event_bus import event_bus
from app.events.event_types import EventType

logger = get_logger(__name__)


class HandController:
    """Controls hand/arm animations via the event bus."""

    def __init__(self) -> None:
        self._current_gesture: Optional[str] = None
        self._lock = asyncio.Lock()

    async def play(self, gesture_name: str, intensity: float = 1.0) -> None:
        """Play a named gesture by publishing animation cue events."""
        async with self._lock:
            frames = GestureLibrary.get(gesture_name, intensity=intensity)
            if frames is None:
                logger.warning("gesture_not_found", gesture=gesture_name)
                return

            self._current_gesture = gesture_name
            await event_bus.publish(
                EventType.GESTURE_STARTED,
                {"gesture": gesture_name, "intensity": intensity},
            )

            # Publish each frame as an animation cue
            total_ms = sum(f.duration_ms for f in frames)
            await event_bus.publish(
                EventType.ANIMATION_REQUESTED,
                {
                    "animation": f"HAND_{gesture_name.upper()}",
                    "target": "hands",
                    "frames": [self._frame_to_dict(f) for f in frames],
                    "total_duration_ms": total_ms,
                    "intensity": intensity,
                },
            )

            # Simulate completion after total duration
            asyncio.create_task(self._finish_after(gesture_name, total_ms / 1000))

    async def _finish_after(self, gesture_name: str, delay_seconds: float) -> None:
        await asyncio.sleep(delay_seconds)
        self._current_gesture = None
        await event_bus.publish(EventType.GESTURE_FINISHED, {"gesture": gesture_name})

    @staticmethod
    def _frame_to_dict(pose: HandPose) -> dict:
        return {
            "left_arm_angle":   pose.left_arm_angle,
            "right_arm_angle":  pose.right_arm_angle,
            "left_elbow_angle": pose.left_elbow_angle,
            "right_elbow_angle": pose.right_elbow_angle,
            "left_open":        pose.left_open,
            "right_open":       pose.right_open,
            "left_wrist":       pose.left_wrist,
            "right_wrist":      pose.right_wrist,
            "duration_ms":      pose.duration_ms,
        }

    # ── Convenience shorthand methods ─────────────────────────────────────────

    async def wave(self, intensity: float = 1.0) -> None:
        await self.play("wave", intensity)

    async def point_right(self) -> None:
        await self.play("point_right")

    async def point_left(self) -> None:
        await self.play("point_left")

    async def thinking_pose(self) -> None:
        await self.play("thinking")

    async def celebrate(self) -> None:
        await self.play("celebrate")

    async def fold_hands(self) -> None:
        await self.play("fold")

    async def open_arms(self) -> None:
        await self.play("open_arms")

    async def explain(self) -> None:
        await self.play("explain")

    @property
    def current_gesture(self) -> Optional[str]:
        return self._current_gesture
