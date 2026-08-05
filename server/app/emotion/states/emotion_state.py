"""EmotionType enum and EmotionState dataclass — core emotion data model."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional


class EmotionType(str, Enum):
    """All supported emotions with their canonical names."""
    NEUTRAL     = "NEUTRAL"
    HAPPY       = "HAPPY"
    SAD         = "SAD"
    EXCITED     = "EXCITED"
    CURIOUS     = "CURIOUS"
    THINKING    = "THINKING"
    CONFUSED    = "CONFUSED"
    ANGRY       = "ANGRY"
    CONCERNED   = "CONCERNED"
    FRIENDLY    = "FRIENDLY"
    PROFESSIONAL = "PROFESSIONAL"
    PROUD       = "PROUD"
    SURPRISED   = "SURPRISED"
    TIRED       = "TIRED"
    LISTENING   = "LISTENING"
    SPEAKING    = "SPEAKING"
    IDLE        = "IDLE"
    SLEEPING    = "SLEEPING"


@dataclass
class EmotionState:
    """A complete snapshot of the robot's current emotional state.

    This drives:
      - Eye shape and blink rate
      - Facial expression
      - Head movement
      - Gesture selection
      - Voice modifier (rate / pitch)
      - Idle animation style
    """

    emotion: EmotionType = EmotionType.NEUTRAL
    intensity: float = 0.5           # 0.0 – 1.0
    onset_time: datetime = field(default_factory=datetime.utcnow)
    decay_rate: float = 0.02         # intensity lost per second while idle

    # What expression, gesture, and movement accompany this emotion
    face_expression: str = "neutral"
    eye_shape: str = "normal"
    blink_rate: str = "normal"       # slow | normal | fast
    head_movement: str = "still"     # still | nod | tilt | shake | look_up
    gesture_hint: str = "idle"       # idle | wave | thinking | celebrate | fold
    voice_rate: float = 1.0          # speech rate multiplier
    voice_pitch: float = 1.0         # pitch multiplier

    def decay(self, elapsed_seconds: float) -> "EmotionState":
        """Return a copy with decayed intensity."""
        new_intensity = max(0.0, self.intensity - self.decay_rate * elapsed_seconds)
        return EmotionState(
            emotion=self.emotion,
            intensity=new_intensity,
            onset_time=self.onset_time,
            decay_rate=self.decay_rate,
            face_expression=self.face_expression,
            eye_shape=self.eye_shape,
            blink_rate=self.blink_rate,
            head_movement=self.head_movement,
            gesture_hint=self.gesture_hint,
            voice_rate=self.voice_rate,
            voice_pitch=self.voice_pitch,
        )

    def to_dict(self) -> dict:
        return {
            "emotion": self.emotion.value,
            "intensity": round(self.intensity, 3),
            "face_expression": self.face_expression,
            "eye_shape": self.eye_shape,
            "blink_rate": self.blink_rate,
            "head_movement": self.head_movement,
            "gesture_hint": self.gesture_hint,
            "voice_rate": self.voice_rate,
            "voice_pitch": self.voice_pitch,
        }
