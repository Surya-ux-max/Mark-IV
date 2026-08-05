"""Gesture library — unified registry of all named gestures.

Usage:
  frames = GestureLibrary.get("wave")
  await hand_controller.play(frames)
"""

from __future__ import annotations

from typing import Callable, Dict, List, Optional

from app.animation.hands.pose import HandPose
from app.animation.hands import (
    celebrate, explain, idle, point, thinking, wave
)


GestureFrames = List[HandPose]
GestureFactory = Callable[[], GestureFrames]


class GestureLibrary:
    """Registry of all available hand gestures."""

    _registry: Dict[str, GestureFactory] = {
        # ── Social ──────────────────────────────────────────────────
        "wave":            lambda: wave.wave(),
        "greeting":        lambda: wave.wave(loops=2, intensity=0.9),
        "bye":             lambda: wave.wave(loops=4, intensity=0.7),

        # ── Pointing ────────────────────────────────────────────────
        "point":           lambda: point.point_forward(),
        "point_right":     lambda: point.point_right(),
        "point_left":      lambda: point.point_left(),

        # ── Celebration ─────────────────────────────────────────────
        "celebrate":       lambda: celebrate.celebrate(),
        "applause":        lambda: celebrate.applause(count=4),

        # ── Cognitive ───────────────────────────────────────────────
        "thinking":        lambda: thinking.thinking_pose(),

        # ── Explanation ─────────────────────────────────────────────
        "explain":         lambda: explain.explain(),
        "open_arms":       lambda: explain.open_arms(),

        # ── Idle / Neutral ───────────────────────────────────────────
        "idle":            lambda: idle.idle_natural(),
        "fold":            lambda: idle.fold_hands(),
        "hands_behind":    lambda: idle.hands_behind_back(),
    }

    @classmethod
    def get(cls, name: str, intensity: float = 1.0) -> Optional[GestureFrames]:
        """Look up and execute a gesture factory by name."""
        factory = cls._registry.get(name.lower())
        if factory is None:
            return None
        return factory()

    @classmethod
    def list_gestures(cls) -> List[str]:
        """Return all available gesture names."""
        return sorted(cls._registry.keys())

    @classmethod
    def register(cls, name: str, factory: GestureFactory) -> None:
        """Register a custom gesture."""
        cls._registry[name.lower()] = factory
