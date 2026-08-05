"""Event dispatcher — wires all modules to the event bus at startup.

Extended to include:
  - Face controller
  - Timeline controller
  - Behavior manager
  - Leg + Hand controllers (via behavior)
  - All new animation events
"""

from __future__ import annotations

from app.core.logging import get_logger
from app.events.event_bus import event_bus

logger = get_logger(__name__)


async def setup_event_subscriptions(
    robot_controller,
    ws_manager,
    emotion_engine,
    face_controller,
    timeline_controller,
    behavior_manager,
) -> None:
    """Wire all subsystem event handlers to the event bus."""
    from app.events.event_types import EventType

    # ── Robot controller ──────────────────────────────────────────────────────
    event_bus.subscribe(EventType.USER_MESSAGE_RECEIVED, robot_controller.on_user_message)
    event_bus.subscribe(EventType.COMMAND_RECEIVED,      robot_controller.on_command)
    event_bus.subscribe(EventType.FACE_DETECTED,         robot_controller.on_face_detected)
    event_bus.subscribe(EventType.FACE_LOST,             robot_controller.on_face_lost)

    # ── WebSocket broadcast ───────────────────────────────────────────────────
    event_bus.subscribe(EventType.ROBOT_STATE_CHANGED,   ws_manager.broadcast_state_change)
    event_bus.subscribe(EventType.ROBOT_STARTED_SPEAKING,ws_manager.broadcast_robot_speaking)
    event_bus.subscribe(EventType.LLM_RESPONSE_READY,    ws_manager.broadcast_robot_response)
    event_bus.subscribe(EventType.EMOTION_CHANGED,       ws_manager.broadcast_emotion)
    event_bus.subscribe(EventType.ANIMATION_REQUESTED,   ws_manager.broadcast_animation)
    event_bus.subscribe(EventType.BLINK,                 ws_manager.broadcast_animation)

    # ── Emotion engine ────────────────────────────────────────────────────────
    event_bus.subscribe(EventType.USER_MESSAGE_RECEIVED, emotion_engine.on_user_message)
    event_bus.subscribe(EventType.LLM_RESPONSE_READY,   emotion_engine.on_robot_response)
    event_bus.subscribe(EventType.FACE_DETECTED,         emotion_engine.on_face_detected)
    event_bus.subscribe(EventType.ROBOT_WOKE_UP,         emotion_engine.on_wake)
    event_bus.subscribe(EventType.ROBOT_WENT_TO_SLEEP,   emotion_engine.on_sleep)
    event_bus.subscribe(EventType.ROBOT_STARTED_THINKING, emotion_engine.on_thinking)

    # ── Face controller ───────────────────────────────────────────────────────
    event_bus.subscribe(EventType.EMOTION_CHANGED,        face_controller.on_emotion_changed)
    event_bus.subscribe(EventType.EXPRESSION_CHANGED,     face_controller.on_expression_changed)
    event_bus.subscribe(EventType.ROBOT_STARTED_SPEAKING, face_controller.on_robot_speaking)
    event_bus.subscribe(EventType.ROBOT_STOPPED_SPEAKING, face_controller.on_robot_stopped_speaking)

    # ── Timeline controller ───────────────────────────────────────────────────
    event_bus.subscribe(EventType.ANIMATION_REQUESTED,   timeline_controller.on_animation_requested)
    event_bus.subscribe(EventType.EXPRESSION_CHANGED,    timeline_controller.on_expression_changed)
    event_bus.subscribe(EventType.GESTURE_STARTED,       timeline_controller.on_gesture_started)
    event_bus.subscribe(EventType.ANIMATION_COMPLETED,   timeline_controller.on_animation_completed)

    # ── Behavior manager ──────────────────────────────────────────────────────
    event_bus.subscribe(EventType.ROBOT_STATE_CHANGED,   behavior_manager.on_robot_state_changed)

    # ── Broadcast expression changes to WS ────────────────────────────────────
    event_bus.subscribe(EventType.EXPRESSION_CHANGED,    ws_manager.broadcast_expression)

    logger.info(
        "event_subscriptions_configured",
        total_subscriptions=event_bus.subscription_count,
    )
