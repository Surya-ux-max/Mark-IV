"""Explain gesture — open-palm explanatory hand movements."""

from __future__ import annotations

from typing import List

from app.animation.hands.pose import HandPose


def explain(intensity: float = 0.8) -> List[HandPose]:
    """Alternating open-palm explaining gestures."""
    arm_angle = 50.0 * intensity
    frames: List[HandPose] = [
        HandPose(right_arm_angle=arm_angle, right_elbow_angle=40.0, right_open=True,
                 left_arm_angle=20.0, left_open=True, duration_ms=350),
        HandPose(right_arm_angle=20.0, right_elbow_angle=20.0, right_open=True,
                 left_arm_angle=arm_angle, left_elbow_angle=40.0, left_open=True, duration_ms=350),
        HandPose(right_arm_angle=arm_angle, right_elbow_angle=40.0, right_open=True,
                 left_arm_angle=20.0, left_open=True, duration_ms=350),
        HandPose(duration_ms=400),  # neutral
    ]
    return frames


def open_arms(intensity: float = 1.0) -> List[HandPose]:
    """Welcoming open-arms gesture."""
    arm_angle = 80.0 * intensity
    return [
        HandPose(left_arm_angle=arm_angle, right_arm_angle=arm_angle,
                 left_elbow_angle=20.0, right_elbow_angle=20.0,
                 left_open=True, right_open=True, duration_ms=500),
        HandPose(left_arm_angle=arm_angle + 10, right_arm_angle=arm_angle + 10,
                 left_open=True, right_open=True, duration_ms=400),
        HandPose(duration_ms=600),
    ]
