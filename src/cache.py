"""Idempotency via content-hash cache (deduplication). Thread-safe, TTL-based."""
from __future__ import annotations
import time
import threading


class InMemoryCache:
    def __init__(self, ttl_s: int = 3600):
        self._ttl = ttl_s
        self._store: dict[str, tuple[str, float]] = {}
        self._lock = threading.Lock()

    def get(self, key: str) -> str | None:
        with self._lock:
            hit = self._store.get(key)
            if not hit:
                return None
            value, ts = hit
            if time.time() - ts > self._ttl:
                self._store.pop(key, None)
                return None
            return value

    def set(self, key: str, value: str) -> None:
        with self._lock:
            self._store[key] = (value, time.time())
