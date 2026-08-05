"""Emotion manager — decides which emotion to transition to given a trigger.

Combines weights, rules, and memory to produce a final emotion decision.
"""

from __future__ import annotations

from typing import Optional, Tuple

from app.emotion.engine.emotion_rules import clamp_intensity, is_allowed
from app.emotion.engine.emotion_transition import build_emotion_state
from app.emotion.engine.emotion_weights import get_weights
from app.emotion.states.emotion_memory import EmotionMemory
from app.emotion.states.emotion_state import EmotionState, EmotionType
from app.core.logging import get_logger

logger = get_logger(__name__)


class EmotionManager:
    """Processes triggers and decides emotion transitions."""

    def __init__(self) -> None:
        self._current: EmotionState = build_emotion_state(EmotionType.NEUTRAL, 0.5)
        self._memory = EmotionMemory(capacity=30)
        self._memory.record(self._current)

    def process_trigger(self, trigger: str) -> Optional[EmotionState]:
        """Apply a trigger and return a new EmotionState if a transition occurs."""
        weights = get_weights(trigger)
        if not weights:
            return None

        # Find the highest-weighted allowed emotion
        best_emotion: Optional[EmotionType] = None
        best_weight: float = 0.0

        for emotion, weight in weights.items():
            if weight > best_weight and is_allowed(
                self._current.emotion, emotion, weight
            ):
                best_emotion = emotion
                best_weight = weight

        if best_emotion is None or best_emotion == self._current.emotion:
            # Boost intensity of current emotion instead of transitioning
            boosted = clamp_intensity(self._current.intensity + best_weight * 0.3)
            if boosted != self._current.intensity:
                self._current = build_emotion_state(self._current.emotion, boosted)
            return None

        new_intensity = clamp_intensity(best_weight)
        new_state = build_emotion_state(best_emotion, new_intensity)

        logger.debug(
            "emotion_transition",
            from_emotion=self._current.emotion.value,
            to_emotion=best_emotion.value,
            intensity=new_intensity,
            trigger=trigger,
        )

        self._memory.record(self._current)
        self._current = new_state
        return new_state

    def set_emotion(self, emotion: EmotionType, intensity: float) -> EmotionState:
        """Forcefully set a specific emotion (e.g., from command)."""
        new_state = build_emotion_state(emotion, clamp_intensity(intensity))
        self._memory.record(self._current)
        self._current = new_state
        return new_state

    def decay(self, elapsed_seconds: float) -> Optional[EmotionState]:
        """Decay current emotion intensity. Returns new state if changed significantly."""
        decayed = self._current.decay(elapsed_seconds)
        if abs(decayed.intensity - self._current.intensity) > 0.01:
            self._current = decayed
            return decayed
        return None

    @property
    def current(self) -> EmotionState:
        return self._current

    @property
    def memory(self) -> EmotionMemory:
        return self._memory
