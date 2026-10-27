"""Use case: single entry point (Single Responsibility, idempotent)."""
from __future__ import annotations
import time
from .config import SETTINGS
from .domain import SimplifyRequest, SimplifyResult
from .languages import get_profile
from .llm_client import LLMPort, LlamaServerClient
from .cache import InMemoryCache
from .ratelimit import RateLimiter, RateLimitedError
from .validator import (
    validate_negations_preserved,
    validate_numbers_preserved,
    validate_output,
)


class ValidationError(ValueError):
    pass


class SimplifyTextUseCase:
    """Validate -> dedupe/cache -> rate-limit -> LLM -> validate -> cache."""

    def __init__(
        self,
        llm: LLMPort | None = None,
        cache: InMemoryCache | None = None,
        limiter: RateLimiter | None = None,
    ):
        self._llm = llm or LlamaServerClient()
        self._cache = cache or InMemoryCache(ttl_s=SETTINGS.cache_ttl_s)
        self._limiter = limiter or RateLimiter(SETTINGS.min_seconds_between_calls)

    def execute(self, req: SimplifyRequest) -> SimplifyResult:
        text = req.normalized
        if len(text) < SETTINGS.min_input_chars:
            raise ValidationError(f"Input too short (min {SETTINGS.min_input_chars} chars)")
        if len(text) > SETTINGS.max_input_chars:
            raise ValidationError(f"Input too long (max {SETTINGS.max_input_chars} chars)")
        if not 0.0 <= req.temperature <= 1.0:
            raise ValidationError("Temperature must be 0-1")
        try:
            profile = get_profile(req.language)
        except ValueError as e:
            raise ValidationError(str(e)) from e

        cached = self._cache.get(req.cache_key)
        if cached is not None:
            return SimplifyResult(
                output=cached, cached=True, model=SETTINGS.model,
                latency_ms=0, language=profile.code,
            )

        try:
            self._limiter.acquire()
        except RateLimitedError as e:
            # Fail closed: no fallback to a fake answer on flood.
            raise ValidationError(str(e)) from e

        t0 = time.monotonic()
        output = self._llm.complete(
            f"{profile.user_prefix}\n\n{text}", req.temperature, profile.system_prompt
        )
        ms = int((time.monotonic() - t0) * 1000)
        if not output:
            raise ValidationError("Empty model output, retry")
        try:
            validate_output(output, profile)
            validate_numbers_preserved(text, output)
            validate_negations_preserved(
                text, output, profile, SETTINGS.min_negation_ratio
            )
        except ValueError as e:
            # Fail closed: never cache unstructured or meaning-inverted output.
            raise ValidationError(f"Invalid model output: {e}") from e
        self._cache.set(req.cache_key, output)
        return SimplifyResult(
            output=output, cached=False, model=SETTINGS.model,
            latency_ms=ms, language=profile.code,
        )
