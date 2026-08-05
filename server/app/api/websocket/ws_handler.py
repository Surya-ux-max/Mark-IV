"""WebSocket endpoint handler — processes all incoming WS messages."""

from __future__ import annotations

import json

from fastapi import WebSocket, WebSocketDisconnect

from app.api.websocket.ws_events import IncomingWSMessage, WelcomeMessage
from app.api.websocket.ws_manager import WSManager
from app.config.constants import WSMessageType
from app.config.settings import Settings
from app.core.logging import get_logger
from app.events.event_bus import event_bus
from app.events.event_types import EventType
from app.robot.controller.robot_controller import RobotController

logger = get_logger(__name__)


async def handle_websocket(
    websocket: WebSocket,
    ws_manager: WSManager,
    robot_controller: RobotController,
    settings: Settings,
) -> None:
    """Handle a single WebSocket client connection lifecycle."""

    session_id = await ws_manager.connect(websocket)

    # Send welcome message
    welcome = WelcomeMessage(
        session_id=session_id,
        robot_name=settings.robot_name,
        state=robot_controller.current_state,
    )
    await ws_manager.send(session_id, welcome.model_dump())

    # Publish connection event
    await event_bus.publish(
        EventType.USER_CONNECTED, {"session_id": session_id}
    )

    try:
        while True:
            raw = await websocket.receive_text()
            await _dispatch_message(
                raw, session_id, ws_manager, robot_controller
            )

    except WebSocketDisconnect:
        logger.info("ws_client_disconnected", session_id=session_id)

    except Exception as exc:
        logger.error("ws_handler_error", session_id=session_id, error=str(exc))

    finally:
        await ws_manager.disconnect(session_id)
        await event_bus.publish(
            EventType.USER_DISCONNECTED, {"session_id": session_id}
        )


async def _dispatch_message(
    raw: str,
    session_id: str,
    ws_manager: WSManager,
    robot_controller: RobotController,
) -> None:
    """Parse and route a raw WebSocket message."""
    try:
        data = json.loads(raw)
        msg = IncomingWSMessage(**data)
    except Exception as exc:
        logger.warning("ws_invalid_message", session_id=session_id, raw=raw[:100], error=str(exc))
        await ws_manager.send(session_id, {"type": "ERROR", "message": "Invalid message format"})
        return

    msg_type = msg.type.upper()
    logger.debug("ws_message_received", type=msg_type, session=session_id)

    if msg_type == WSMessageType.USER_MESSAGE:
        text = (msg.text or "").strip()
        if text:
            await event_bus.publish(
                EventType.USER_MESSAGE_RECEIVED,
                {"text": text, "session_id": session_id},
            )

    elif msg_type == WSMessageType.COMMAND:
        command = (msg.command or "").upper()
        await event_bus.publish(
            EventType.COMMAND_RECEIVED,
            {"command": command, "session_id": session_id},
        )

    elif msg_type == WSMessageType.USER_STARTED_SPEAKING:
        await event_bus.publish(
            EventType.USER_STARTED_SPEAKING, {"session_id": session_id}
        )

    elif msg_type == WSMessageType.USER_STOPPED_SPEAKING:
        await event_bus.publish(
            EventType.USER_STOPPED_SPEAKING, {"session_id": session_id}
        )

    elif msg_type == "SPEAKING_DONE":
        # Client signals that browser TTS finished speaking
        await robot_controller.notify_speaking_done(session_id)

    elif msg_type == WSMessageType.FACE_DETECTED:
        data = msg.data or {}
        await event_bus.publish(
            EventType.FACE_DETECTED,
            {
                "face_id": data.get("face_id", "unknown"),
                "position": data.get("position", {}),
                "confidence": data.get("confidence", 1.0),
                "session_id": session_id,
            },
        )

    elif msg_type == WSMessageType.PING:
        await ws_manager.send(session_id, {"type": "PONG"})

    else:
        logger.debug("ws_unknown_message_type", type=msg_type)
