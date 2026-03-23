"""Audio transcription service — uses OpenAI Whisper API via Euri to transcribe audio."""

import logging
import tempfile
from pathlib import Path

from app.security import safe_filename
from app.services.euri_client import euri_client

logger = logging.getLogger(__name__)


def transcribe_audio(file_bytes: bytes, filename: str) -> str:
    """Transcribe audio using OpenAI Whisper API via Euri.

    Falls back to empty string if transcription fails.
    """
    sanitized = safe_filename(filename)
    with tempfile.TemporaryDirectory() as tmpdir:
        audio_path = Path(tmpdir) / sanitized
        audio_path.write_bytes(file_bytes)

        try:
            with open(audio_path, "rb") as f:
                response = euri_client.audio.transcriptions.create(
                    model="whisper-1",
                    file=f,
                )
            transcript = response.text or ""
            logger.info("Transcribed %s: %s", sanitized, transcript[:100])
            return transcript
        except Exception:
            logger.exception("Whisper transcription failed for %s, falling back to metadata", sanitized)
            return ""
