"""App config - single source of truth (DRY)."""
from dataclasses import dataclass

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

SETTINGS = Settings()
