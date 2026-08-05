"""Expression library — maps emotion names to full face descriptor dicts.

Each expression describes:
  - mouth shape
  - eyebrow position
  - eye shape
  - cheek color
  - blink rate (ms between blinks)
  - transition_ms (how long to animate to this expression)
"""

from __future__ import annotations

from typing import Dict


# ── Expression profiles ──────────────────────────────────────────────────────

EXPRESSIONS: Dict[str, dict] = {
    "neutral": dict(
        mouth="flat",       eyebrow="normal",    eye="normal",
        cheek=None,         blink_ms=4000,       transition_ms=400,
    ),
    "smile": dict(
        mouth="smile",      eyebrow="raised",    eye="happy",
        cheek="pink",       blink_ms=3000,       transition_ms=350,
    ),
    "sad": dict(
        mouth="frown",      eyebrow="drooped",   eye="droopy",
        cheek=None,         blink_ms=5000,       transition_ms=600,
    ),
    "excited": dict(
        mouth="open_smile", eyebrow="raised",    eye="wide",
        cheek="red",        blink_ms=2000,       transition_ms=200,
    ),
    "curious": dict(
        mouth="slight_smile", eyebrow="one_up",  eye="raised_brow",
        cheek=None,          blink_ms=3500,      transition_ms=350,
    ),
    "thinking": dict(
        mouth="flat",       eyebrow="furrowed",  eye="look_up",
        cheek=None,         blink_ms=5500,       transition_ms=400,
    ),
    "confused": dict(
        mouth="open",       eyebrow="furrowed",  eye="furrowed",
        cheek=None,         blink_ms=5000,       transition_ms=500,
    ),
    "angry": dict(
        mouth="frown",      eyebrow="lowered",   eye="furrowed",
        cheek=None,         blink_ms=3000,       transition_ms=300,
    ),
    "concerned": dict(
        mouth="slight_frown", eyebrow="drooped", eye="furrowed",
        cheek=None,           blink_ms=4500,     transition_ms=450,
    ),
    "attentive": dict(
        mouth="flat",       eyebrow="raised",    eye="wide",
        cheek=None,         blink_ms=5000,       transition_ms=300,
    ),
    "speaking": dict(
        mouth="talking",    eyebrow="normal",    eye="normal",
        cheek=None,         blink_ms=3500,       transition_ms=100,
    ),
    "proud": dict(
        mouth="smile",      eyebrow="raised",    eye="confident",
        cheek="pink",       blink_ms=3000,       transition_ms=400,
    ),
    "surprised": dict(
        mouth="open",       eyebrow="raised_high", eye="wide",
        cheek="pink",       blink_ms=2500,       transition_ms=150,
    ),
    "tired": dict(
        mouth="flat",       eyebrow="drooped",   eye="droopy",
        cheek=None,         blink_ms=7000,       transition_ms=800,
    ),
    "sleeping": dict(
        mouth="flat",       eyebrow="normal",    eye="closed",
        cheek=None,         blink_ms=0,          transition_ms=1200,
    ),
}


def get_expression(name: str) -> dict:
    """Get expression profile by name, falling back to neutral."""
    return EXPRESSIONS.get(name, EXPRESSIONS["neutral"])
