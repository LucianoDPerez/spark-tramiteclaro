"""Best-effort OS locale detection (no framework imports, never raises)."""
from __future__ import annotations

import locale
import os
import subprocess

from .languages import DEFAULT_LANGUAGE, PROFILES


def _code_from_tag(raw: str | None) -> str | None:
    if not raw:
        return None
    # Handles "es_AR.UTF-8", "zh_CN", "en_US.UTF-8@euro", "es-AR"
    base = raw.split(".")[0].split("@")[0].replace("-", "_")
    code = base.split("_")[0].lower()
    return code if code in PROFILES else None


def _apple_locale() -> str | None:
    """macOS stores the user's language in AppleLocale (e.g. 'es_AR')."""
    try:
        out = subprocess.run(
            ["defaults", "read", "-g", "AppleLocale"],
            capture_output=True, timeout=3,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if out.returncode != 0:
        return None
    return out.stdout.decode("utf-8", errors="replace").strip()


def detect_language() -> str:
    """Return the closest supported language for the current OS user."""
    for raw in (
        os.environ.get("LC_ALL"),
        os.environ.get("LC_MESSAGES"),
        os.environ.get("LANG"),
        _apple_locale(),
    ):
        code = _code_from_tag(raw)
        if code:
            return code
    try:
        code = _code_from_tag(locale.getlocale()[0])
        if code:
            return code
    except (ValueError, TypeError):
        pass
    return DEFAULT_LANGUAGE
