"""Typed publisher helpers — each subsystem uses these to publish events.

These are thin helpers that ensure the correct payload shape is
used for each event type, making publishing intent explicit.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from app.events.event_bus import event_bus
from app.events.event_types import EventType


class SpeechPublisher:
    @staticmethod
    async def user_started_speaking(session_id: str) -> None:
        await event_bus.publish(EventType.USER_STARTED_SPEAKING, {"session_id": session_id})

    @staticmethod
    async def user_stopped_speaking(session_id: str) -> None:
        await event_bus.publish(EventType.USER_STOPPED_SPEAKING, {"session_id": session_id})

    @staticmethod
    async def user_message_received(text: str, session_id: str) -> None:
        await event_bus.publish(
            EventType.USER_MESSAGE_RECEIVED, {"text": text, "session_id": session_id}
        )


class RobotPublisher:
    @staticmethod
    async def state_changed(previous: str, new: str, emotion: str = "NEUTRAL") -> None:
        await event_bus.publish(
            EventType.ROBOT_STATE_CHANGED,
            {"previous_state": previous, "new_state": new, "emotion": emotion},
        )

    @staticmethod
    async def started_speaking(text: str, session_id: Optional[str] = None) -> None:
        await event_bus.publish(
            EventType.ROBOT_STARTED_SPEAKING,
            {"text": text, "session_id": session_id},
        )

    @staticmethod
    async def stopped_speaking(session_id: Optional[str] = None) -> None:
        await event_bus.publish(
            EventType.ROBOT_STOPPED_SPEAKING, {"session_id": session_id}
        )

    @staticmethod
    async def woke_up() -> None:
        await event_bus.publish(EventType.ROBOT_WOKE_UP, {})

    @staticmethod
    async def went_to_sleep() -> None:
        await event_bus.publish(EventType.ROBOT_WENT_TO_SLEEP, {})

    @staticmethod
    async def started_thinking(session_id: Optional[str] = None) -> None:
        await event_bus.publish(
            EventType.ROBOT_STARTED_THINKING, {"session_id": session_id}
        )

    @staticmethod
    async def finished_thinking(session_id: Optional[str] = None) -> None:
        await event_bus.publish(
            EventType.ROBOT_FINISHED_THINKING, {"session_id": session_id}
        )


class EmotionPublisher:
    @staticmethod
    async def emotion_changed(
        emotion: str, intensity: float = 0.5, trigger: Optional[str] = None
    ) -> None:
        await event_bus.publish(
            EventType.EMOTION_CHANGED,
            {"emotion": emotion, "intensity": intensity, "trigger": trigger},
        )


class AnimationPublisher:
    @staticmethod
    async def request(
        animation: str, params: Optional[Dict[str, Any]] = None, duration_ms: Optional[int] = None
    ) -> None:
        await event_bus.publish(
            EventType.ANIMATION_REQUESTED,
            {"animation": animation, "params": params or {}, "duration_ms": duration_ms},
        )

    @staticmethod
    async def blink() -> None:
        await event_bus.publish(EventType.BLINK, {"animation": "BLINK"})

    @staticmethod
    async def look_at_person(face_id: str, position: Dict[str, float]) -> None:
        await event_bus.publish(
            EventType.LOOK_AT_PERSON, {"face_id": face_id, "position": position}
        )


class VisionPublisher:
    @staticmethod
    async def face_detected(face_id: str, position: Dict[str, float], confidence: float) -> None:
        await event_bus.publish(
            EventType.FACE_DETECTED,
            {"face_id": face_id, "position": position, "confidence": confidence},
        )

    @staticmethod
    async def face_lost(face_id: str) -> None:
        await event_bus.publish(EventType.FACE_LOST, {"face_id": face_id})


class LLMPublisher:
    @staticmethod
    async def response_ready(
        text: str, session_id: Optional[str], sources: Optional[List[str]] = None
    ) -> None:
        await event_bus.publish(
            EventType.LLM_RESPONSE_READY,
            {"text": text, "session_id": session_id, "sources": sources or []},
        )
