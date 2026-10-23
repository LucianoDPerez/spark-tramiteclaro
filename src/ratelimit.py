"""Minimal rate limiter: protects single-slot llama-server from flooding."""
from __future__ import annotations
import time
import threading


class RateLimitedError(RuntimeError):
    pass


class RateLimiter:
    def __init__(self, min_interval_s: float = 2.0):
        self._min = min_interval_s
        self._last: float = 0.0
        self._lock = threading.Lock()

    def acquire(self) -> None:
        with self._lock:
            now = time.monotonic()
            delta = now - self._last
            if delta < self._min:
                raise RateLimitedError(f"Wait {self._min - delta:.1f}s between requests")
            self._last = now
