"""WebSocket server configuration."""

from dataclasses import dataclass


@dataclass(frozen=True)
class WebSocketConfig:
    """WebSocket server parameters."""

    heartbeat_interval: int = 30       # seconds between PING/PONG
    max_connections: int = 50
    max_message_size: int = 65536      # 64 KB
    connection_timeout: int = 300      # 5 minutes
    close_timeout: int = 10
