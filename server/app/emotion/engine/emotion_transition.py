"""Emotion transition — builds fully-populated EmotionState for each emotion type.

This is the single source of truth for what each emotion looks like
across eyes, face, head, gestures, and voice.
"""

from __future__ import annotations

from app.emotion.states.emotion_state import EmotionState, EmotionType


# ── Emotion → full behavioral descriptor ─────────────────────────────────────
_EMOTION_PROFILES: dict[EmotionType, dict] = {
    EmotionType.NEUTRAL: dict(
        face_expression="neutral", eye_shape="normal", blink_rate="normal",
        head_movement="still", gesture_hint="idle",
        voice_rate=1.0, voice_pitch=1.0, decay_rate=0.005,
    ),
    EmotionType.HAPPY: dict(
        face_expression="smile", eye_shape="happy", blink_rate="fast",
        head_movement="nod", gesture_hint="wave",
        voice_rate=1.1, voice_pitch=1.05, decay_rate=0.02,
    ),
    EmotionType.SAD: dict(
        face_expression="sad", eye_shape="droopy", blink_rate="slow",
        head_movement="tilt", gesture_hint="fold",
        voice_rate=0.85, voice_pitch=0.9, decay_rate=0.01,
    ),
    EmotionType.EXCITED: dict(
        face_expression="excited", eye_shape="wide", blink_rate="fast",
        head_movement="nod", gesture_hint="celebrate",
        voice_rate=1.2, voice_pitch=1.1, decay_rate=0.03,
    ),
    EmotionType.CURIOUS: dict(
        face_expression="curious", eye_shape="raised_brow", blink_rate="normal",
        head_movement="tilt", gesture_hint="point",
        voice_rate=1.0, voice_pitch=1.02, decay_rate=0.02,
    ),
    EmotionType.THINKING: dict(
        face_expression="thinking", eye_shape="look_up", blink_rate="slow",
        head_movement="tilt", gesture_hint="thinking",
        voice_rate=0.9, voice_pitch=0.98, decay_rate=0.015,
    ),
    EmotionType.CONFUSED: dict(
        face_expression="confused", eye_shape="furrowed", blink_rate="slow",
        head_movement="shake", gesture_hint="fold",
        voice_rate=0.85, voice_pitch=0.95, decay_rate=0.015,
    ),
    EmotionType.ANGRY: dict(
        face_expression="angry", eye_shape="furrowed", blink_rate="normal",
        head_movement="still", gesture_hint="fold",
        voice_rate=0.95, voice_pitch=0.9, decay_rate=0.02,
    ),
    EmotionType.CONCERNED: dict(
        face_expression="concerned", eye_shape="furrowed", blink_rate="slow",
        head_movement="tilt", gesture_hint="fold",
        voice_rate=0.9, voice_pitch=0.95, decay_rate=0.015,
    ),
    EmotionType.FRIENDLY: dict(
        face_expression="smile", eye_shape="happy", blink_rate="normal",
        head_movement="nod", gesture_hint="wave",
        voice_rate=1.05, voice_pitch=1.02, decay_rate=0.02,
    ),
    EmotionType.PROFESSIONAL: dict(
        face_expression="neutral", eye_shape="normal", blink_rate="normal",
        head_movement="still", gesture_hint="explain",
        voice_rate=0.95, voice_pitch=1.0, decay_rate=0.01,
    ),
    EmotionType.PROUD: dict(
        face_expression="proud", eye_shape="confident", blink_rate="normal",
        head_movement="nod", gesture_hint="celebrate",
        voice_rate=1.0, voice_pitch=1.05, decay_rate=0.02,
    ),
    EmotionType.SURPRISED: dict(
        face_expression="surprised", eye_shape="wide", blink_rate="fast",
        head_movement="still", gesture_hint="open_arms",
        voice_rate=1.1, voice_pitch=1.1, decay_rate=0.04,
    ),
    EmotionType.TIRED: dict(
        face_expression="tired", eye_shape="droopy", blink_rate="slow",
        head_movement="still", gesture_hint="idle",
        voice_rate=0.85, voice_pitch=0.9, decay_rate=0.005,
    ),
    EmotionType.LISTENING: dict(
        face_expression="attentive", eye_shape="wide", blink_rate="slow",
        head_movement="nod", gesture_hint="fold",
        voice_rate=1.0, voice_pitch=1.0, decay_rate=0.01,
    ),
    EmotionType.SPEAKING: dict(
        face_expression="speaking", eye_shape="normal", blink_rate="normal",
        head_movement="still", gesture_hint="explain",
        voice_rate=1.0, voice_pitch=1.0, decay_rate=0.01,
    ),
    EmotionType.IDLE: dict(
        face_expression="neutral", eye_shape="normal", blink_rate="slow",
        head_movement="still", gesture_hint="idle",
        voice_rate=1.0, voice_pitch=1.0, decay_rate=0.003,
    ),
    EmotionType.SLEEPING: dict(
        face_expression="sleeping", eye_shape="closed", blink_rate="none",
        head_movement="still", gesture_hint="idle",
        voice_rate=0.8, voice_pitch=0.85, decay_rate=0.001,
    ),
}


def build_emotion_state(emotion: EmotionType, intensity: float) -> EmotionState:
    """Create a fully-populated EmotionState for a given emotion and intensity."""
    profile = _EMOTION_PROFILES.get(emotion, _EMOTION_PROFILES[EmotionType.NEUTRAL])
    return EmotionState(
        emotion=emotion,
        intensity=intensity,
        **profile,
    )
