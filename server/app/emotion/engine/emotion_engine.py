"""Full Emotion Engine — continuously manages robot emotional state.

Subscribes to all relevant events, delegates to EmotionManager for
transition decisions, publishes EMOTION_CHANGED + animation cues.
"""

from __future__ import annotations

import asyncio
import random
import time
from typing import Any, Optional

from app.core.logging import get_logger
from app.emotion.engine.emotion_manager import EmotionManager
from app.emotion.states.emotion_state import EmotionState, EmotionType
from app.events.event_types import EventType
from app.events.publishers import AnimationPublisher, EmotionPublisher

logger = get_logger(__name__)

# Map EventType values to emotion trigger keys
_EVENT_TRIGGER_MAP: dict[str, str] = {
    EventType.USER_MESSAGE_RECEIVED:  "USER_MESSAGE_RECEIVED",
    EventType.FACE_DETECTED:          "FACE_DETECTED",
    EventType.FACE_LOST:              "FACE_LOST",
    EventType.ROBOT_WOKE_UP:          "ROBOT_WOKE_UP",
    EventType.ROBOT_WENT_TO_SLEEP:    "ROBOT_WENT_TO_SLEEP",
    EventType.ROBOT_STARTED_THINKING: "ROBOT_STARTED_THINKING",
    EventType.LLM_RESPONSE_READY:     "LLM_RESPONSE_READY",
    EventType.SYSTEM_ERROR:           "ERROR",
}


class EmotionEngine:
    """Central emotion controller for SurveX robot.

    Integrates:
      - EmotionManager for weight-based transition logic
      - Blink loop for natural eye animation
      - Decay loop for emotional fade-over-time
      - Event-driven emotion triggers
    """

    def __init__(self) -> None:
        self._manager = EmotionManager()
        self._blink_task: Optional[asyncio.Task] = None
        self._decay_task: Optional[asyncio.Task] = None
        self._last_tick: float = time.monotonic()

    async def initialize(self) -> None:
        self._blink_task = asyncio.create_task(self._blink_loop())
        self._decay_task = asyncio.create_task(self._decay_loop())
        logger.info("emotion_engine_ready", emotion=self._manager.current.emotion.value)

    async def shutdown(self) -> None:
        for task in (self._blink_task, self._decay_task):
            if task:
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass

    # ── Blink loop ────────────────────────────────────────────────────────────

    async def _blink_loop(self) -> None:
        while True:
            try:
                emotion = self._manager.current.emotion
                # Blink rate varies by emotion
                if emotion in (EmotionType.SLEEPING, EmotionType.TIRED):
                    interval = random.uniform(6.0, 10.0)
                elif emotion in (EmotionType.EXCITED, EmotionType.HAPPY, EmotionType.SURPRISED):
                    interval = random.uniform(1.5, 3.0)
                else:
                    interval = random.uniform(3.0, 5.5)
                await asyncio.sleep(interval)
                await AnimationPublisher.blink()
            except asyncio.CancelledError:
                break
            except Exception as exc:
                logger.warning("blink_loop_error", error=str(exc))

    # ── Decay loop ────────────────────────────────────────────────────────────

    async def _decay_loop(self) -> None:
        while True:
            try:
                await asyncio.sleep(2.0)
                now = time.monotonic()
                elapsed = now - self._last_tick
                self._last_tick = now
                decayed = self._manager.decay(elapsed)
                if decayed:
                    await self._publish_emotion(decayed, trigger="decay")
            except asyncio.CancelledError:
                break
            except Exception as exc:
                logger.warning("decay_loop_error", error=str(exc))

    # ── Internal publish ──────────────────────────────────────────────────────

    async def _publish_emotion(self, state: EmotionState, trigger: str = "") -> None:
        """Publish EMOTION_CHANGED + animation cues derived from the new state."""
        await EmotionPublisher.emotion_changed(
            emotion=state.emotion.value,
            intensity=state.intensity,
            trigger=trigger,
        )
        # Publish expression cue
        await AnimationPublisher.request(
            animation="EXPRESSION_CHANGED",
            params=state.to_dict(),
        )
        # Publish gesture hint
        if state.gesture_hint not in ("idle", ""):
            await AnimationPublisher.request(
                animation=f"HAND_{state.gesture_hint.upper()}",
                params={"intensity": state.intensity},
                duration_ms=2000,
            )
        # Publish head movement hint
        if state.head_movement != "still":
            await AnimationPublisher.request(
                animation=f"HEAD_{state.head_movement.upper()}",
                params={"intensity": state.intensity * 0.6},
                duration_ms=1500,
            )

    async def _apply_trigger(self, trigger: str) -> None:
        new_state = self._manager.process_trigger(trigger)
        if new_state:
            await self._publish_emotion(new_state, trigger=trigger)

    # ── Event handlers ────────────────────────────────────────────────────────

    async def on_user_message(self, event_type: str, payload: Any) -> None:
        await self._apply_trigger("USER_MESSAGE_RECEIVED")

    async def on_robot_response(self, event_type: str, payload: Any) -> None:
        await self._apply_trigger("LLM_RESPONSE_READY")

    async def on_face_detected(self, event_type: str, payload: Any) -> None:
        await self._apply_trigger("FACE_DETECTED")

    async def on_wake(self, event_type: str, payload: Any) -> None:
        await self._apply_trigger("ROBOT_WOKE_UP")

    async def on_sleep(self, event_type: str, payload: Any) -> None:
        new_state = self._manager.set_emotion(EmotionType.SLEEPING, 0.9)
        await self._publish_emotion(new_state, trigger="sleep_command")

    async def on_thinking(self, event_type: str, payload: Any) -> None:
        await self._apply_trigger("ROBOT_STARTED_THINKING")

    # ── Public API ────────────────────────────────────────────────────────────

    @property
    def current_emotion(self) -> EmotionType:
        return self._manager.current.emotion

    @property
    def current_state(self) -> EmotionState:
        return self._manager.current
