"""System-wide constants and enumerations."""

from enum import Enum


# ── Robot States ─────────────────────────────────────────────────────────────

class RobotState(str, Enum):
    SLEEPING = "SLEEPING"
    IDLE = "IDLE"
    LISTENING = "LISTENING"
    THINKING = "THINKING"
    SPEAKING = "SPEAKING"
    GREETING = "GREETING"
    OBSERVING = "OBSERVING"
    ERROR = "ERROR"


# ── Emotions ─────────────────────────────────────────────────────────────────

class Emotion(str, Enum):
    NEUTRAL = "NEUTRAL"
    HAPPY = "HAPPY"
    CURIOUS = "CURIOUS"
    THINKING = "THINKING"
    SURPRISED = "SURPRISED"
    EMPATHETIC = "EMPATHETIC"
    EXCITED = "EXCITED"
    CALM = "CALM"
    CONFUSED = "CONFUSED"


# ── Intent Types ─────────────────────────────────────────────────────────────

class IntentType(str, Enum):
    GREETING = "GREETING"
    FAREWELL = "FAREWELL"
    QUESTION = "QUESTION"
    KNOWLEDGE_QUERY = "KNOWLEDGE_QUERY"
    COMMAND = "COMMAND"
    FEEDBACK = "FEEDBACK"
    CHITCHAT = "CHITCHAT"
    UNKNOWN = "UNKNOWN"


# ── WebSocket Message Types ───────────────────────────────────────────────────

class WSMessageType(str, Enum):
    # Client → Server
    COMMAND = "COMMAND"
    USER_MESSAGE = "USER_MESSAGE"
    USER_STARTED_SPEAKING = "USER_STARTED_SPEAKING"
    USER_STOPPED_SPEAKING = "USER_STOPPED_SPEAKING"
    FACE_DETECTED = "FACE_DETECTED"
    FACE_LOST = "FACE_LOST"
    PING = "PING"

    # Server → Client
    STATE_CHANGED = "STATE_CHANGED"
    ROBOT_RESPONSE = "ROBOT_RESPONSE"
    EMOTION_CHANGED = "EMOTION_CHANGED"
    ANIMATION_CUE = "ANIMATION_CUE"
    KNOWLEDGE_CONTEXT = "KNOWLEDGE_CONTEXT"
    ERROR = "ERROR"
    PONG = "PONG"
    WELCOME = "WELCOME"


# ── Commands ──────────────────────────────────────────────────────────────────

class RobotCommand(str, Enum):
    WAKE_UP = "WAKE_UP"
    SLEEP = "SLEEP"
    RESET = "RESET"
    STOP_SPEAKING = "STOP_SPEAKING"


# ── Animation Types ───────────────────────────────────────────────────────────

class AnimationType(str, Enum):
    BLINK = "BLINK"
    NOD = "NOD"
    SHAKE_HEAD = "SHAKE_HEAD"
    WAVE = "WAVE"
    POINT = "POINT"
    THINKING_LOOK = "THINKING_LOOK"
    EYE_TRACK = "EYE_TRACK"
    IDLE_SWAY = "IDLE_SWAY"
    SPEAK_MOUTH = "SPEAK_MOUTH"
    SLEEP_CLOSE = "SLEEP_CLOSE"
    WAKE_OPEN = "WAKE_OPEN"


# ── Limits ────────────────────────────────────────────────────────────────────

MAX_MESSAGE_LENGTH: int = 2000
MAX_RESPONSE_TOKENS: int = 512
MIN_CONFIDENCE_SCORE: float = 0.15
BLINK_INTERVAL_SECONDS: float = 4.0
IDLE_ANIMATION_INTERVAL: float = 8.0
WS_HEARTBEAT_INTERVAL: int = 30  # seconds
