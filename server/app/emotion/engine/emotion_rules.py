"""Emotion rules — allowed transitions and constraints between emotions.

Prevents invalid jumps (e.g., SLEEPING → EXCITED without going through NEUTRAL first).
"""

from __future__ import annotations

from typing import Dict, Set

from app.emotion.states.emotion_state import EmotionType

E = EmotionType

# All emotions that can be freely transitioned into from any state
UNIVERSAL_TARGETS: Set[EmotionType] = {E.NEUTRAL, E.IDLE}

# Explicit allowed transitions (source → {allowed targets})
# If a target is not listed, the transition is allowed by default unless restricted
RESTRICTED_SOURCES: Dict[EmotionType, Set[EmotionType]] = {
    E.SLEEPING: {E.NEUTRAL, E.HAPPY, E.IDLE},  # must wake up first
    E.ANGRY:    {E.CONCERNED, E.NEUTRAL, E.CONFUSED, E.SAD},
}

# Minimum intensity to trigger a transition (prevents micro-fluctuations)
MIN_TRANSITION_INTENSITY: float = 0.3


def is_allowed(from_emotion: EmotionType, to_emotion: EmotionType, intensity: float) -> bool:
    """Return True if the transition from_emotion → to_emotion is permitted."""
    if intensity < MIN_TRANSITION_INTENSITY:
        return False
    if to_emotion in UNIVERSAL_TARGETS:
        return True
    if from_emotion in RESTRICTED_SOURCES:
        return to_emotion in RESTRICTED_SOURCES[from_emotion]
    return True


def clamp_intensity(intensity: float) -> float:
    return max(0.0, min(1.0, intensity))
