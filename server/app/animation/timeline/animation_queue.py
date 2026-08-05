"""Animation queue — priority queue of pending animation frames."""

from __future__ import annotations

import asyncio
from typing import Optional

from app.animation.timeline.animation_frame import AnimationFrame


class AnimationQueue:
    """Priority queue for animation frames.

    Higher-priority frames preempt lower-priority ones.
    Parallel frames (face + hands) can run simultaneously.
    """

    def __init__(self) -> None:
        # Per-target queues: only one animation per target at a time
        self._queues: dict[str, asyncio.PriorityQueue] = {}
        self._active: dict[str, Optional[AnimationFrame]] = {}

    def _get_queue(self, target: str) -> asyncio.PriorityQueue:
        if target not in self._queues:
            self._queues[target] = asyncio.PriorityQueue()
            self._active[target] = None
        return self._queues[target]

    async def enqueue(self, frame: AnimationFrame) -> None:
        """Add a frame to its target queue."""
        q = self._get_queue(frame.target)
        # Negate priority so highest priority = lowest queue value
        await q.put((-frame.priority, id(frame), frame))

    async def dequeue(self, target: str) -> Optional[AnimationFrame]:
        """Get next frame for a target, or None if empty."""
        q = self._queues.get(target)
        if q is None or q.empty():
            return None
        try:
            _, _, frame = q.get_nowait()
            self._active[target] = frame
            return frame
        except asyncio.QueueEmpty:
            return None

    def clear_target(self, target: str) -> None:
        """Clear all pending frames for a target."""
        if target in self._queues:
            while not self._queues[target].empty():
                try:
                    self._queues[target].get_nowait()
                except asyncio.QueueEmpty:
                    break
            self._active[target] = None

    @property
    def active_targets(self) -> dict:
        return {t: f for t, f in self._active.items() if f}
