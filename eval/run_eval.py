"""Fact-retention harness: runs the real local model on synthetic cases.

Usage: python3 -m eval.run_eval [--lang es] [--out eval/results.json]
Needs llama-server on :8080. Never fabricates output: failures are recorded.
"""
from __future__ import annotations

import argparse
import json
import statistics
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from eval.cases import CASES  # noqa: E402
from src.domain import SimplifyRequest  # noqa: E402
from src.languages import get_profile  # noqa: E402
from src.usecase import SimplifyTextUseCase, ValidationError  # noqa: E402


def norm(text: str) -> str:
    text = " ".join(text.lower().split())
    return "".join(
        c for c in unicodedata.normalize("NFD", text)
        if unicodedata.category(c) != "Mn"
    )


def retained_facts(facts: list[str], output: str) -> list[str]:
    body = norm(output)
    return [f for f in facts if norm(f) in body]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lang", help="only run cases for this language")
    ap.add_argument("--out", default="eval/results.json")
    args = ap.parse_args()

    cases = [c for c in CASES if not args.lang or c["language"] == args.lang]
    uc = SimplifyTextUseCase()
    rows: list[dict] = []

    for case in cases:
        profile = get_profile(case["language"])
        row = {
            "id": case["id"],
            "language": case["language"],
            "facts_total": len(case["facts"]),
            "status": "ok",
            "cached": False,
            "latency_ms": 0,
            "missing_facts": [],
            "error": None,
            "output": "",
        }
        try:
            res = uc.execute(
                SimplifyRequest(text=case["text"], language=case["language"])
            )
            row.update(
                cached=res.cached,
                latency_ms=res.latency_ms,
                output=res.output,
            )
            missing = []
            kept = retained_facts(case["facts"], res.output)
            row["missing_facts"] = [f for f in case["facts"] if f not in kept]
        except ValidationError as e:
            # Fail-closed rejection is a recorded outcome, not a crash.
            row.update(status="rejected", error=str(e))
        except Exception as e:  # noqa: BLE001 - record, never hide
            row.update(status="error", error=f"{type(e).__name__}: {e}")
        rows.append(row)
        mark = "ok" if row["status"] == "ok" else row["status"]
        kept_n = row["facts_total"] - len(row["missing_facts"])
        print(
            f"{row['id']:<16} {profile.label:<8} {mark:<9} "
            f"facts {kept_n}/{row['facts_total']}  {row['latency_ms']}ms"
        )

    Path(args.out).write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")

    ok_rows = [r for r in rows if r["status"] == "ok"]
    total_facts = sum(r["facts_total"] for r in ok_rows)
    kept_facts = sum(r["facts_total"] - len(r["missing_facts"]) for r in ok_rows)
    if ok_rows:
        p50 = statistics.median(r["latency_ms"] for r in ok_rows)
        print(f"\nfacts retained: {kept_facts}/{total_facts} "
              f"({len(ok_rows)}/{len(rows)} cases accepted)")
        print(f"median latency: {p50:.0f}ms")
    else:
        print(f"\nno case accepted ({len(rows)} attempted)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
