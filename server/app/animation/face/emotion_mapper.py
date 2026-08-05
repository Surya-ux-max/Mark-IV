"""Emotion → expression mapper.

Translates EmotionType values to face expression names and
publishes EXPRESSION_CHANGED events.
"""

from __future__ import annotations

from app.animation.face.expression_library import get_expression
from app.core.logging import get_logger
from app.events.event_bus import event_bus
from app.events.event_types import EventType

logger = get_logger(__name__)

# emotion name → expression name
_EMOTION_TO_EXPRESSION: dict[str, str] = {
    "NEUTRAL":      "neutral",
    "HAPPY":        "smile",
    "SAD":          "sad",
    "EXCITED":      "excited",
    "CURIOUS":      "curious",
    "THINKING":     "thinking",
    "CONFUSED":     "confused",
    "ANGRY":        "angry",
    "CONCERNED":    "concerned",
    "FRIENDLY":     "smile",
    "PROFESSIONAL": "neutral",
    "PROUD":        "proud",
    "SURPRISED":    "surprised",
    "TIRED":        "tired",
    "LISTENING":    "attentive",
    "SPEAKING":     "speaking",
    "IDLE":         "neutral",
    "SLEEPING":     "sleeping",
}


class EmotionMapper:
    """Maps emotions to expressions and publishes expression change events."""

    @staticmethod
    def emotion_to_expression(emotion: str) -> str:
        return _EMOTION_TO_EXPRESSION.get(emotion.upper(), "neutral")

    @staticmethod
    async def apply_emotion(emotion: str, intensity: float = 0.7) -> None:
        """Publish an EXPRESSION_CHANGED event for an emotion."""
        expression_name = EmotionMapper.emotion_to_expression(emotion)
        expression = get_expression(expression_name)
        await event_bus.publish(
            EventType.EXPRESSION_CHANGED,
            {
                "expression": expression_name,
                "emotion": emotion,
                "intensity": intensity,
                **expression,
            },
        )
        logger.debug(
            "expression_applied",
            emotion=emotion,
            expression=expression_name,
        )
