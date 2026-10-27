"""App config - single source of truth (DRY)."""
from dataclasses import dataclass
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent


@dataclass(frozen=True)
class Settings:
    base_url: str = "http://localhost:8080/v1"
    model: str = "spark2.6-4B"
    timeout_s: int = 120
    max_tokens: int = 1200
    default_temp: float = 0.2
    max_input_chars: int = 4000
    min_input_chars: int = 20
    # Anti-flood for local llama-server (single slot, 16k ctx).
    min_seconds_between_calls: float = 2.0
    cache_ttl_s: int = 3600

    # Negation preservation: ratio of negation markers that must survive.
    # 1.0 = every negation in the input must appear in the output (fail-closed).
    # Per-language markers live in src/languages.py (owned by each profile).
    min_negation_ratio: float = 1.0

    # Text-to-speech (offline, macOS `say`).
    tts_voice: str = "Paulina"
    tts_words_per_minute: int = 150
    tts_timeout_s: int = 60

    # OCR (offline, local tesseract + bundled spa.traineddata).
    ocr_lang: str = "spa"
    ocr_timeout_s: int = 60
    ocr_tessdata: Path = PROJECT_ROOT / "models" / "tessdata"


SETTINGS = Settings()
