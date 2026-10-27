"""OCR port + local tesseract adapter (offline photo-to-text)."""
from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Protocol

from .config import SETTINGS


class OCRError(RuntimeError):
    pass


class OCRPort(Protocol):
    def read_text(self, image_bytes: bytes, lang: str) -> str:
        ...


class TesseractOCR:
    """Offline OCR. Uses the bundled traineddata, never uploads the image."""

    def __init__(
        self,
        tessdata: Path = SETTINGS.ocr_tessdata,
        timeout_s: int = SETTINGS.ocr_timeout_s,
    ):
        self._tessdata = tessdata
        self._timeout = timeout_s

    @staticmethod
    def available() -> bool:
        return shutil.which("tesseract") is not None

    def read_text(self, image_bytes: bytes, lang: str) -> str:
        if not image_bytes:
            raise OCRError("Empty image")
        if not self.available():
            raise OCRError("tesseract not installed")
        if not (self._tessdata / f"{lang}.traineddata").exists():
            raise OCRError(f"OCR language data missing for '{lang}'")

        env = {**os.environ, "TESSDATA_PREFIX": str(self._tessdata)}
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / "input.png"
            src.write_bytes(image_bytes)
            try:
                proc = subprocess.run(
                    ["tesseract", str(src), "stdout", "-l", lang, "--psm", "6"],
                    capture_output=True,
                    timeout=self._timeout,
                    env=env,
                )
            except (OSError, subprocess.SubprocessError) as e:
                raise OCRError("OCR failed") from e
        if proc.returncode != 0:
            raise OCRError("OCR failed")
        text = " ".join(proc.stdout.decode("utf-8", errors="replace").split())
        if not text:
            raise OCRError("No readable text found in image")
        return text
