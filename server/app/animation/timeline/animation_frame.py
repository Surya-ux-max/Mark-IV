"""Animation frame — the atomic unit of the animation timeline."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class AnimationFrame:
    """A single scheduled animation event.

    Fields:
        animation   : Named animation identifier (e.g. "HAND_WAVE")
        target      : Body part target ("hands", "legs", "face", "head", "body")
        params      : Animation parameters dict
        duration_ms : How long this frame lasts
        priority    : Higher priority preempts lower (0=lowest, 10=highest)
        interruptible: Can this frame be interrupted?
        parallel    : Can this run alongside other animations?
    """

    animation: str
    target: str = "body"
    params: Dict[str, Any] = field(default_factory=dict)
    duration_ms: int = 1000
    priority: int = 5
    interruptible: bool = True
    parallel: bool = False
    loop: bool = False
    frames: list = field(default_factory=list)  # sub-frames for complex anims

    def to_ws_payload(self) -> dict:
        """Convert to WebSocket animation cue payload."""
        return {
            "animation": self.animation,
            "target": self.target,
            "params": self.params,
            "duration_ms": self.duration_ms,
            "priority": self.priority,
            "loop": self.loop,
            "frames": self.frames,
        }
