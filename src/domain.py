"""Domain entities. No framework imports here (Clean Architecture)."""
from __future__ import annotations
import hashlib
from dataclasses import dataclass

from .languages import DEFAULT_LANGUAGE


def normalize(text: str) -> str:
    """Collapse whitespace for deduplication (same intent -> same key)."""
    return " ".join(text.strip().split())


@dataclass(frozen=True)
class SimplifyRequest:
    text: str
    temperature: float = 0.2
    language: str = DEFAULT_LANGUAGE

    @property
    def normalized(self) -> str:
        return normalize(self.text)

    @property
    def cache_key(self) -> str:
        raw = f"{self.normalized}|temp={self.temperature}|lang={self.language}"
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:32]


@dataclass(frozen=True)
class SimplifyResult:
    output: str
    cached: bool
    model: str
    latency_ms: int
    language: str = DEFAULT_LANGUAGE
