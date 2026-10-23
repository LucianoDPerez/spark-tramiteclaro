"""LLM port + llama-server adapter (Dependency Inversion)."""
from __future__ import annotations
from typing import Protocol
import requests
from .config import SETTINGS
from .prompts import SYSTEM_PROMPT


class LLMError(RuntimeError):
    pass


class LLMPort(Protocol):
    def complete(self, text: str, temperature: float) -> str:
        ...


class LlamaServerClient:
    """Thin adapter over local OpenAI-compatible endpoint. No dynamic URLs (SSRF-safe)."""

    def __init__(self, base_url: str = SETTINGS.base_url, model: str = SETTINGS.model):
        self._url = base_url.rstrip("/") + "/chat/completions"
        self._model = model

    def complete(self, text: str, temperature: float) -> str:
        payload = {
            "model": self._model,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Explicá este texto:\n\n{text}"},
            ],
            "temperature": temperature,
            "top_p": 0.95,
            "max_tokens": SETTINGS.max_tokens,
            # Spark-X2.6 thinks by default and fills the budget without answering.
            "chat_template_kwargs": {"enable_thinking": False},
        }
        try:
            r = requests.post(self._url, json=payload, timeout=SETTINGS.timeout_s)
            r.raise_for_status()
            data = r.json()
        except requests.RequestException as e:
            # Never leak internals beyond a short message (OWASP: error handling).
            raise LLMError("LLM server unreachable on :8080") from e
        try:
            return str(data["choices"][0]["message"]["content"]).strip()
        except (KeyError, IndexError, TypeError) as e:
            raise LLMError("Unexpected LLM response shape") from e
