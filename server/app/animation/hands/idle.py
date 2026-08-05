"""Idle hand animations — subtle natural movements when robot is waiting."""

from __future__ import annotations

from typing import List

from app.animation.hands.pose import FOLD_POSE, NEUTRAL_POSE, HandPose


def idle_natural() -> List[HandPose]:
    """Gentle natural idle sway with arms at sides."""
    return [
        HandPose(left_arm_angle=-5.0, right_arm_angle=5.0, duration_ms=2000),
        HandPose(left_arm_angle=5.0, right_arm_angle=-5.0, duration_ms=2000),
        NEUTRAL_POSE,
    ]


def hands_behind_back() -> List[HandPose]:
    """Professional stance — hands behind back."""
    return [
        HandPose(left_arm_angle=-40.0, right_arm_angle=-40.0,
                 left_elbow_angle=60.0, right_elbow_angle=60.0,
                 left_open=False, right_open=False,
                 left_wrist=-20.0, right_wrist=20.0,
                 duration_ms=600),
    ]


def fold_hands() -> List[HandPose]:
    """Politely folded hands at front."""
    return [FOLD_POSE]
