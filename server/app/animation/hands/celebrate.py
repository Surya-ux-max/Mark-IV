"""Celebrate / applause gesture."""

from __future__ import annotations

from typing import List

from app.animation.hands.pose import HandPose


def celebrate(intensity: float = 1.0) -> List[HandPose]:
    """Both arms raise to celebrate — like a victory cheer."""
    arm_angle = 140.0 * intensity
    return [
        HandPose(left_arm_angle=arm_angle, right_arm_angle=arm_angle,
                 left_open=True, right_open=True, duration_ms=400),
        HandPose(left_arm_angle=arm_angle - 15, right_arm_angle=arm_angle + 15,
                 left_open=True, right_open=True, duration_ms=200),
        HandPose(left_arm_angle=arm_angle + 15, right_arm_angle=arm_angle - 15,
                 left_open=True, right_open=True, duration_ms=200),
        HandPose(left_arm_angle=arm_angle, right_arm_angle=arm_angle,
                 left_open=True, right_open=True, duration_ms=300),
        HandPose(left_arm_angle=0.0, right_arm_angle=0.0,
                 left_open=True, right_open=True, duration_ms=500),
    ]


def applause(count: int = 3) -> List[HandPose]:
    """Hands clap together."""
    frames: List[HandPose] = []
    for _ in range(count):
        frames.append(HandPose(
            left_arm_angle=40.0, right_arm_angle=40.0,
            left_elbow_angle=70.0, right_elbow_angle=70.0,
            left_open=False, right_open=False, duration_ms=120,
        ))
        frames.append(HandPose(
            left_arm_angle=30.0, right_arm_angle=30.0,
            left_elbow_angle=50.0, right_elbow_angle=50.0,
            left_open=True, right_open=True, duration_ms=120,
        ))
    frames.append(HandPose(duration_ms=400))  # neutral
    return frames
