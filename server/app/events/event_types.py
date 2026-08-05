"""All event type names used by the SurveX event bus."""

from enum import Enum


class EventType(str, Enum):
    """Enum of all publishable event types.

    Naming convention: <SUBJECT>_<VERB_PAST_TENSE>
    """

    # ── System ────────────────────────────────────────────────────────────────
    SYSTEM_READY = "SYSTEM_READY"
    SYSTEM_SHUTDOWN = "SYSTEM_SHUTDOWN"
    SYSTEM_ERROR = "SYSTEM_ERROR"

    # ── Robot Lifecycle ───────────────────────────────────────────────────────
    ROBOT_WOKE_UP = "ROBOT_WOKE_UP"
    ROBOT_WENT_TO_SLEEP = "ROBOT_WENT_TO_SLEEP"
    ROBOT_STATE_CHANGED = "ROBOT_STATE_CHANGED"
    ROBOT_STARTED_SPEAKING = "ROBOT_STARTED_SPEAKING"
    ROBOT_STOPPED_SPEAKING = "ROBOT_STOPPED_SPEAKING"
    ROBOT_STARTED_THINKING = "ROBOT_STARTED_THINKING"
    ROBOT_FINISHED_THINKING = "ROBOT_FINISHED_THINKING"

    # ── User / Speech ─────────────────────────────────────────────────────────
    USER_STARTED_SPEAKING = "USER_STARTED_SPEAKING"
    USER_STOPPED_SPEAKING = "USER_STOPPED_SPEAKING"
    USER_MESSAGE_RECEIVED = "USER_MESSAGE_RECEIVED"
    USER_CONNECTED = "USER_CONNECTED"
    USER_DISCONNECTED = "USER_DISCONNECTED"
    USER_DETECTED = "USER_DETECTED"
    USER_LEFT = "USER_LEFT"

    # ── LLM / Knowledge ───────────────────────────────────────────────────────
    LLM_RESPONSE_READY = "LLM_RESPONSE_READY"
    KNOWLEDGE_RETRIEVED = "KNOWLEDGE_RETRIEVED"
    CONTEXT_UPDATED = "CONTEXT_UPDATED"

    # ── Emotion ───────────────────────────────────────────────────────────────
    EMOTION_CHANGED = "EMOTION_CHANGED"
    MOOD_UPDATED = "MOOD_UPDATED"
    EMOTION_TRANSITION_STARTED = "EMOTION_TRANSITION_STARTED"
    EMOTION_TRANSITION_FINISHED = "EMOTION_TRANSITION_FINISHED"

    # ── Vision ────────────────────────────────────────────────────────────────
    FACE_DETECTED = "FACE_DETECTED"
    FACE_LOST = "FACE_LOST"
    PERSON_ENTERED = "PERSON_ENTERED"
    PERSON_LEFT = "PERSON_LEFT"
    OBJECT_DETECTED = "OBJECT_DETECTED"
    HAND_GESTURE = "HAND_GESTURE"

    # ── Hand / Gesture ────────────────────────────────────────────────────────
    GESTURE_STARTED = "GESTURE_STARTED"
    GESTURE_FINISHED = "GESTURE_FINISHED"
    HAND_WAVE = "HAND_WAVE"
    HAND_POINT = "HAND_POINT"
    HAND_CELEBRATE = "HAND_CELEBRATE"
    HAND_THINKING = "HAND_THINKING"
    HAND_FOLD = "HAND_FOLD"
    HAND_OPEN_ARMS = "HAND_OPEN_ARMS"
    HAND_IDLE = "HAND_IDLE"

    # ── Leg / Movement ────────────────────────────────────────────────────────
    WALK_FORWARD = "WALK_FORWARD"
    STOP_WALKING = "STOP_WALKING"
    TURN_LEFT = "TURN_LEFT"
    TURN_RIGHT = "TURN_RIGHT"
    STEP_FORWARD = "STEP_FORWARD"
    STEP_BACKWARD = "STEP_BACKWARD"
    IDLE_STANCE = "IDLE_STANCE"

    # ── Face / Expression ─────────────────────────────────────────────────────
    EXPRESSION_CHANGED = "EXPRESSION_CHANGED"
    BLINK = "BLINK"
    LOOK_LEFT = "LOOK_LEFT"
    LOOK_RIGHT = "LOOK_RIGHT"
    LOOK_UP = "LOOK_UP"
    LOOK_DOWN = "LOOK_DOWN"
    HEAD_NOD = "HEAD_NOD"
    HEAD_SHAKE = "HEAD_SHAKE"
    HEAD_TILT = "HEAD_TILT"

    # ── Animation ─────────────────────────────────────────────────────────────
    ANIMATION_REQUESTED = "ANIMATION_REQUESTED"
    ANIMATION_COMPLETED = "ANIMATION_COMPLETED"
    LOOK_AT_PERSON = "LOOK_AT_PERSON"
    LOOK_AWAY = "LOOK_AWAY"

    # ── Behavior ──────────────────────────────────────────────────────────────
    BEHAVIOR_TRIGGERED = "BEHAVIOR_TRIGGERED"
    BEHAVIOR_STARTED = "BEHAVIOR_STARTED"
    BEHAVIOR_FINISHED = "BEHAVIOR_FINISHED"

    # ── Commands ──────────────────────────────────────────────────────────────
    COMMAND_RECEIVED = "COMMAND_RECEIVED"
