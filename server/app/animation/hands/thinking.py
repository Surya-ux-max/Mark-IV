"""Thinking pose — right hand to chin, head tilted."""

from __future__ import annotations

from typing import List

from app.animation.hands.pose import HandPose


def thinking_pose(hold_ms: int = 3000) -> List[HandPose]:
    """Classic thinking pose: right elbow bent, hand near face."""
    return [
        HandPose(
            right_arm_angle=45.0, right_elbow_angle=90.0,
            right_wrist=15.0, right_open=False,
            left_arm_angle=20.0, left_elbow_angle=30.0,
            duration_ms=500,
        ),
        # Hold pose
        HandPose(
            right_arm_angle=48.0, right_elbow_angle=88.0,
            right_wrist=18.0, right_open=False,
            left_arm_angle=20.0, left_elbow_angle=30.0,
            duration_ms=hold_ms,
        ),
        # Return
        HandPose(duration_ms=500),
    ]
