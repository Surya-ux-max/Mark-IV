"""Virtual TTS service stub.

In virtual robot mode, TTS is handled by the browser's SpeechSynthesis API.
The server sends the response TEXT to the client, and the browser speaks it.

To enable server-side TTS (for physical robot):
  1. Install edge-tts: uv add edge-tts
  2. Replace this stub with a real TTS implementation
  3. Stream audio bytes back to client or robot speaker
"""

from __future__ import annotations

from app.core.interfaces import ITTSService
from app.core.logging import get_logger

logger = get_logger(__name__)


class VirtualTTSService(ITTSService):
    """Virtual TTS — sends text to client; browser synthesizes speech."""

    async def initialize(self) -> None:
        logger.info("tts_virtual_mode_active")

    async def shutdown(self) -> None:
        pass

    async def synthesize(self, text: str) -> bytes:
        """Virtual synthesis — client handles real TTS via Web Speech API."""
        logger.debug("tts_virtual_synthesize_called", text=text[:50])
        return b""  # No audio bytes in virtual mode
