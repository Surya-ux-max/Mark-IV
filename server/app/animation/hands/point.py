"""Point gesture — directional pointing with right or left hand."""

from __future__ import annotations

from typing import List

from app.animation.hands.pose import HandPose


def point_right(intensity: float = 1.0) -> List[HandPose]:
    arm_angle = 70.0 * intensity
    return [
        HandPose(right_arm_angle=arm_angle, right_elbow_angle=0.0, right_open=False, duration_ms=350),
        HandPose(right_arm_angle=arm_angle + 5.0, right_open=False, duration_ms=200),
        HandPose(right_arm_angle=0.0, right_elbow_angle=0.0, right_open=True, duration_ms=400),
    ]


def point_left(intensity: float = 1.0) -> List[HandPose]:
    arm_angle = 70.0 * intensity
    return [
        HandPose(left_arm_angle=arm_angle, left_elbow_angle=0.0, left_open=False, duration_ms=350),
        HandPose(left_arm_angle=arm_angle + 5.0, left_open=False, duration_ms=200),
        HandPose(left_arm_angle=0.0, left_elbow_angle=0.0, left_open=True, duration_ms=400),
    ]


def point_forward(intensity: float = 1.0) -> List[HandPose]:
    arm_angle = 60.0 * intensity
    return [
        HandPose(right_arm_angle=arm_angle, right_elbow_angle=10.0, right_open=False, duration_ms=300),
        HandPose(right_arm_angle=arm_angle, right_open=False, duration_ms=500),
        HandPose(right_arm_angle=0.0, right_elbow_angle=0.0, right_open=True, duration_ms=400),
    ]
