"""Face controller — orchestrates all facial animations.

Subscribes to EMOTION_CHANGED and EXPRESSION_CHANGED events
and publishes the appropriate animation cues to the frontend.
"""

from __future__ import annotations

from typing import Any

from app.animation.face.emotion_mapper import EmotionMapper
from app.animation.face.expression_library import get_expression
from app.core.logging import get_logger
from app.events.event_bus import event_bus
from app.events.event_types import EventType

logger = get_logger(__name__)


class FaceController:
    """Controls all facial animation in response to emotion events."""

    def __init__(self) -> None:
        self._current_expression: str = "neutral"

    async def on_emotion_changed(self, event_type: str, payload: Any) -> None:
        """Respond to EMOTION_CHANGED by updating face expression."""
        emotion = payload.get("emotion", "NEUTRAL")
        intensity = payload.get("intensity", 0.5)
        await EmotionMapper.apply_emotion(emotion, intensity)

    async def on_expression_changed(self, event_type: str, payload: Any) -> None:
        """Forward EXPRESSION_CHANGED to frontend as animation cue."""
        expression = payload.get("expression", "neutral")
        self._current_expression = expression
        await event_bus.publish(
            EventType.ANIMATION_REQUESTED,
            {
                "animation": "FACE_EXPRESSION",
                "target": "face",
                "expression": expression,
                "params": {k: v for k, v in payload.items()
                           if k not in ("expression", "emotion")},
            },
        )

    async def on_robot_speaking(self, event_type: str, payload: Any) -> None:
        await EmotionMapper.apply_emotion("SPEAKING", intensity=0.8)

    async def on_robot_stopped_speaking(self, event_type: str, payload: Any) -> None:
        # Revert to the pre-speaking expression
        await EmotionMapper.apply_emotion("NEUTRAL", intensity=0.5)

    async def set_expression(self, name: str) -> None:
        """Directly set a named expression."""
        expression = get_expression(name)
        self._current_expression = name
        await event_bus.publish(
            EventType.EXPRESSION_CHANGED,
            {"expression": name, **expression},
        )

    @property
    def current_expression(self) -> str:
        return self._current_expression
