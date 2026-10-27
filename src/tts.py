"""Text-to-speech port + macOS adapter (offline, no cloud)."""
from __future__ import annotations

import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Protocol

from .config import SETTINGS


class TTSError(RuntimeError):
    pass


class TTSPort(Protocol):
    def synthesize(self, text: str, voice: str) -> bytes:
        """Return WAV audio bytes for the given text."""
        ...


class MacSayTTS:
    """Offline TTS via macOS `say`. Writes PCM WAV, never leaves the machine."""

    def __init__(
        self,
        words_per_minute: int = SETTINGS.tts_words_per_minute,
        timeout_s: int = SETTINGS.tts_timeout_s,
    ):
        self._wpm = words_per_minute
        self._timeout = timeout_s

    @staticmethod
    def available() -> bool:
        return shutil.which("say") is not None

    def synthesize(self, text: str, voice: str = SETTINGS.tts_voice) -> bytes:
        if not text.strip():
            raise TTSError("Nothing to read")
        if not self.available():
            raise TTSError("`say` not available on this system")
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            out = Path(tmp.name)
        try:
            proc = subprocess.run(
                [
                    "say",
                    "-v", voice,
                    "-r", str(self._wpm),
                    "--data-format=LEI16@22050",
                    "-o", str(out),
                    text,
                ],
                capture_output=True,
                timeout=self._timeout,
            )
            if proc.returncode != 0:
                raise TTSError(f"TTS failed for voice '{voice}'")
            return out.read_bytes()
        except (OSError, subprocess.SubprocessError) as e:
            raise TTSError("TTS failed") from e
        finally:
            out.unlink(missing_ok=True)
