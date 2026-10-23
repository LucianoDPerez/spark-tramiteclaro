# AGENTS.md — TramiteClaro local

Instructions for AI coding agents working in this repo. Follow them strictly.

## What this is

HER Hack-Astron #7 entry. Offline-first plain-language explainer for official/health texts, powered at runtime by local Spark-X2.6-4B via llama-server (`http://localhost:8080/v1`). No cloud calls. No diagnosis.

## How to run

1. Model must be up: `curl http://localhost:8080/health` -> `{"status":"ok"}`. Model id `spark2.6-4B`. If down, tell the user to start it (command in README.md). Never fake outputs.
2. App: `.venv/bin/python -m streamlit run app.py` (port 8501).
3. CLI: `.venv/bin/python simplificar.py <file>`.
4. Tests (no model needed): `python3 -m unittest -v` — must stay green.

## Architecture (do not break)

- `src/config.py` — single source of truth. No magic numbers elsewhere.
- `src/domain.py` — pure entities, no framework imports. `normalize()` + `cache_key` implement deduplication.
- `src/usecase.py` — `SimplifyTextUseCase.execute()` is the ONLY path to the LLM. Validate -> cache -> rate-limit -> LLM -> cache. Idempotent by content hash.
- `src/llm_client.py` — `LLMPort` protocol + `LlamaServerClient`. Fixed URL only (no SSRF). Always send `chat_template_kwargs: {enable_thinking: False}` — Spark-X2.6 fills the token budget with reasoning otherwise and returns empty content.
- `src/cache.py`, `src/ratelimit.py` — thread-safe, TTL / min-interval. Fail closed.
- `src/prompts.py` — Spanish system prompt. Output MUST keep 3 fixed sections + safety footer. Never add diagnosis or dosage.
- UI (`app.py`, `simplificar.py`) — thin layers. No business logic, no direct `requests` to LLM.

## Rules

- SOLID / Clean / KISS / DRY. One responsibility per file. Inject fakes for tests (see `test_usecase.py`), never call the real model in unit tests.
- Validate inputs: 20–4000 chars, temp 0–1. Reject with `ValidationError`, never traceback internals.
- Never log full user texts or PII. Never commit secrets, tokens, or personal data. `outputs/` and `docs/shot-*` contain only generic hand-written examples.
- Keep `docs/DISCUSSION.md` in sync with code: revision `fe31f8d64890302cc3a1d365d700357b4b75ba77`, Q4_K_M, ctx 16384, temp 0.2/top-p 0.95/top-k 20/repeat-penalty 1.05.
- Report failures honestly (e.g. EX1 fasting phrasing). Do not invent model outputs.
