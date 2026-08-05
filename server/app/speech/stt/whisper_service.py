"""Virtual STT service stub.

In virtual robot mode, STT is handled by the browser's Web Speech API.
This stub provides the interface for future Whisper integration.

To enable real STT:
  1. Set VIRTUAL_MODE=false in config
  2. Replace this stub with a real Whisper implementation
  3. The rest of the system doesn't change
"""

from __future__ import annotations

from app.core.interfaces import ISTTService
from app.core.logging import get_logger

logger = get_logger(__name__)


class VirtualSTTService(ISTTService):
    """Virtual STT — accepts text directly (browser handles real STT)."""

    async def initialize(self) -> None:
        logger.info("stt_virtual_mode_active")

    async def shutdown(self) -> None:
        pass

    async def transcribe(self, audio_data: bytes) -> str:
        """Virtual transcription — returns empty (browser does real STT)."""
        logger.debug("stt_virtual_transcribe_called")
        return ""
