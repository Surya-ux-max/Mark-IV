"""Vision subsystem configuration (virtual mode defaults)."""

from dataclasses import dataclass


@dataclass(frozen=True)
class VisionConfig:
    """Camera and CV parameters — virtual mode defaults."""

    camera_id: int = 0
    frame_width: int = 640
    frame_height: int = 480
    fps: int = 30
    face_detection_threshold: float = 0.6
    object_detection_threshold: float = 0.5
    gesture_detection_threshold: float = 0.7

    # Virtual mode: vision events injected from WebSocket client
    virtual_mode: bool = True
