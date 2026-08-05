"""Animation timeline — dispatches animation cues to frontend via event bus.

When the robot state changes, this module publishes the appropriate
ANIMATION_REQUESTED events, which WSManager broadcasts to the client.
The client's React components respond to these events to animate the robot.
"""

from __future__ import annotations

from typing import Any

from app.config.constants import AnimationType
from app.core.logging import get_logger
from app.events.publishers import AnimationPublisher

logger = get_logger(__name__)


class AnimationTimeline:
    """Coordinates animation cues in response to robot lifecycle events."""

    async def on_emotion_changed(self, event_type: str, payload: Any) -> None:
        emotion = payload.get("emotion", "NEUTRAL")
        await AnimationPublisher.request(
            animation="EMOTION_EXPRESSION",
            params={"emotion": emotion, "intensity": payload.get("intensity", 0.5)},
        )

    async def on_robot_speaking(self, event_type: str, payload: Any) -> None:
        await AnimationPublisher.request(
            animation=AnimationType.SPEAK_MOUTH,
            params={"active": True},
        )

    async def on_robot_stopped(self, event_type: str, payload: Any) -> None:
        await AnimationPublisher.request(
            animation=AnimationType.SPEAK_MOUTH,
            params={"active": False},
        )

    async def on_thinking(self, event_type: str, payload: Any) -> None:
        await AnimationPublisher.request(
            animation=AnimationType.THINKING_LOOK,
            params={"active": True},
            duration_ms=3000,
        )

    async def on_wake(self, event_type: str, payload: Any) -> None:
        await AnimationPublisher.request(
            animation=AnimationType.WAKE_OPEN,
            params={},
            duration_ms=800,
        )

    async def on_sleep(self, event_type: str, payload: Any) -> None:
        await AnimationPublisher.request(
            animation=AnimationType.SLEEP_CLOSE,
            params={},
            duration_ms=1200,
        )
