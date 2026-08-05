"""Movement library — registry of all named leg movements.

Usage:
  frames = MovementLibrary.get("walk")
  await leg_controller.play(frames)
"""

from __future__ import annotations

from typing import Callable, Dict, List, Optional

from app.animation.legs.leg_pose import LegPose
from app.animation.legs import idle, turn, walk

MovementFrames = List[LegPose]
MovementFactory = Callable[[], MovementFrames]


class MovementLibrary:
    """Registry of all available leg movements."""

    _registry: Dict[str, MovementFactory] = {
        "walk":         lambda: walk.walk_cycle(steps=4),
        "walk_fast":    lambda: walk.walk_cycle(steps=4, speed=1.5),
        "idle_sway":    lambda: idle.idle_sway(),
        "idle_bounce":  lambda: idle.idle_bounce(),
        "turn_left":    lambda: turn.turn_left(45.0),
        "turn_right":   lambda: turn.turn_right(45.0),
    }

    @classmethod
    def get(cls, name: str) -> Optional[MovementFrames]:
        factory = cls._registry.get(name.lower())
        return factory() if factory else None

    @classmethod
    def list_movements(cls) -> List[str]:
        return sorted(cls._registry.keys())
