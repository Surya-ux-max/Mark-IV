"""WebSocket connection manager — manages all active client connections."""

from __future__ import annotations

import uuid
from typing import Any, Dict, Optional, Set

from fastapi import WebSocket

from app.api.websocket.ws_events import (
    AnimationCueMessage,
    EmotionChangedMessage,
    RobotResponseMessage,
    StateChangedMessage,
)
from app.core.logging import get_logger

logger = get_logger(__name__)


class WSManager:
    """Manages WebSocket connections and broadcasts events to all clients."""

    def __init__(self) -> None:
        self._connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket) -> str:
        """Accept a new WebSocket connection and return its session ID."""
        await websocket.accept()
        session_id = str(uuid.uuid4())[:8]
        self._connections[session_id] = websocket
        logger.info("ws_connected", session_id=session_id, total=len(self._connections))
        return session_id

    async def disconnect(self, session_id: str) -> None:
        """Remove a disconnected client."""
        self._connections.pop(session_id, None)
        logger.info("ws_disconnected", session_id=session_id, remaining=len(self._connections))

    async def send(self, session_id: str, message: dict) -> None:
        """Send a message to a specific client."""
        ws = self._connections.get(session_id)
        if ws:
            try:
                await ws.send_json(message)
            except Exception as exc:
                logger.warning("ws_send_failed", session_id=session_id, error=str(exc))
                await self.disconnect(session_id)

    async def broadcast(self, message: dict) -> None:
        """Broadcast a message to ALL connected clients."""
        dead: list[str] = []
        for sid, ws in self._connections.items():
            try:
                await ws.send_json(message)
            except Exception:
                dead.append(sid)
        for sid in dead:
            await self.disconnect(sid)

    # ── Event bus handler callbacks ───────────────────────────────────────────

    async def broadcast_state_change(self, event_type: str, payload: Any) -> None:
        msg = StateChangedMessage(
            state=payload.get("new_state", "IDLE"),
            emotion=payload.get("emotion", "NEUTRAL"),
            is_awake=payload.get("new_state", "") != "SLEEPING",
        )
        await self.broadcast(msg.model_dump())

    async def broadcast_robot_speaking(self, event_type: str, payload: Any) -> None:
        """Broadcast the response text so client can initiate TTS."""
        session_id: Optional[str] = payload.get("session_id")
        text: str = payload.get("text", "")
        msg = RobotResponseMessage(text=text, session_id=session_id)
        if session_id and session_id in self._connections:
            await self.send(session_id, msg.model_dump())
        else:
            await self.broadcast(msg.model_dump())

    async def broadcast_robot_response(self, event_type: str, payload: Any) -> None:
        """Broadcast LLM_RESPONSE_READY with sources."""
        session_id: Optional[str] = payload.get("session_id")
        msg = RobotResponseMessage(
            text=payload.get("text", ""),
            session_id=session_id,
            sources=payload.get("sources", []),
        )
        if session_id and session_id in self._connections:
            await self.send(session_id, msg.model_dump())
        else:
            await self.broadcast(msg.model_dump())

    async def broadcast_emotion(self, event_type: str, payload: Any) -> None:
        msg = EmotionChangedMessage(
            emotion=payload.get("emotion", "NEUTRAL"),
            intensity=payload.get("intensity", 0.5),
        )
        await self.broadcast(msg.model_dump())

    async def broadcast_animation(self, event_type: str, payload: Any) -> None:
        msg = AnimationCueMessage(
            animation=payload.get("animation", "BLINK"),
            params=payload.get("params", {}),
            duration_ms=payload.get("duration_ms"),
        )
        await self.broadcast(msg.model_dump())

    async def broadcast_expression(self, event_type: str, payload: Any) -> None:
        """Broadcast facial expression change to all clients."""
        await self.broadcast({
            "type": "EXPRESSION_CHANGED",
            "expression": payload.get("expression", "neutral"),
            "emotion": payload.get("emotion", "NEUTRAL"),
            "intensity": payload.get("intensity", 0.5),
            "mouth": payload.get("mouth", "flat"),
            "eye_shape": payload.get("eye_shape", "normal"),
            "eyebrow": payload.get("eyebrow", "normal"),
            "blink_rate": payload.get("blink_rate", "normal"),
            "cheek": payload.get("cheek"),
            "transition_ms": payload.get("transition_ms", 400),
        })

    @property
    def connection_count(self) -> int:
        return len(self._connections)

    @property
    def session_ids(self) -> Set[str]:
        return set(self._connections.keys())
