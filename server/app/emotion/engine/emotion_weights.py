"""Emotion weights — maps incoming events to emotion deltas.

Each trigger maps to a dict of {EmotionType: weight} showing how strongly
that trigger pushes the robot toward each emotion.
"""

from __future__ import annotations

from typing import Dict

from app.emotion.states.emotion_state import EmotionType

# Shorthand aliases
E = EmotionType

# ── Trigger → emotion weight mappings ────────────────────────────────────────
TRIGGER_WEIGHTS: Dict[str, Dict[EmotionType, float]] = {

    "USER_MESSAGE_RECEIVED": {
        E.CURIOUS:      0.5,
        E.LISTENING:    0.4,
        E.FRIENDLY:     0.3,
    },
    "GREETING_RECEIVED": {
        E.HAPPY:        0.8,
        E.FRIENDLY:     0.7,
        E.EXCITED:      0.4,
    },
    "FAREWELL_RECEIVED": {
        E.FRIENDLY:     0.5,
        E.NEUTRAL:      0.3,
        E.SAD:          0.2,
    },
    "KNOWLEDGE_QUERY": {
        E.CURIOUS:      0.6,
        E.THINKING:     0.5,
        E.PROFESSIONAL: 0.4,
    },
    "QUESTION_RECEIVED": {
        E.CURIOUS:      0.6,
        E.THINKING:     0.4,
    },
    "LLM_RESPONSE_READY": {
        E.SPEAKING:     0.7,
        E.PROUD:        0.2,
        E.FRIENDLY:     0.3,
    },
    "FACE_DETECTED": {
        E.HAPPY:        0.5,
        E.EXCITED:      0.3,
        E.FRIENDLY:     0.4,
    },
    "FACE_LOST": {
        E.NEUTRAL:      0.4,
        E.TIRED:        0.2,
    },
    "ROBOT_WOKE_UP": {
        E.HAPPY:        0.7,
        E.EXCITED:      0.5,
        E.FRIENDLY:     0.5,
    },
    "ROBOT_WENT_TO_SLEEP": {
        E.TIRED:        0.6,
        E.SLEEPING:     0.9,
    },
    "ROBOT_STARTED_THINKING": {
        E.THINKING:     0.8,
        E.CURIOUS:      0.4,
    },
    "ERROR": {
        E.CONCERNED:    0.7,
        E.CONFUSED:     0.4,
    },
    "LONG_SILENCE": {
        E.IDLE:         0.6,
        E.TIRED:        0.3,
    },
    "COMPLIMENT_RECEIVED": {
        E.HAPPY:        0.7,
        E.PROUD:        0.6,
        E.EXCITED:      0.4,
    },
    "CONFUSION_DETECTED": {
        E.CONFUSED:     0.7,
        E.CONCERNED:    0.4,
    },
}


def get_weights(trigger: str) -> Dict[EmotionType, float]:
    """Return emotion weights for a given trigger, or empty dict if unknown."""
    return TRIGGER_WEIGHTS.get(trigger, {})
