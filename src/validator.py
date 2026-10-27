"""Output validator: fail-closed structure check (Clean Architecture, no I/O)."""
from __future__ import annotations

import re

REQUIRED_HEADERS = (
    "VERSIÓN SIMPLE:",
    "PASOS A SEGUIR:",
    "QUÉ LLEVAR / QUÉ PREGUNTAR:",
)

SAFETY_FOOTER = "Esto es una ayuda explicativa, no reemplaza al profesional."


def _cleaned(output: str) -> str:
    # Model sometimes wraps headers in markdown bold (**...**). Strip it.
    return output.replace("*", "")


def validate_output(output: str) -> None:
    """Raise ValueError if output breaks the 3-section + footer contract."""
    if not output or not output.strip():
        raise ValueError("Empty model output")
    text = _cleaned(output)
    missing = [h for h in REQUIRED_HEADERS if h not in text]
    if missing:
        raise ValueError(f"Missing sections: {', '.join(missing)}")
    if SAFETY_FOOTER not in text:
        raise ValueError("Missing safety footer")
    # Order matters: prevents reordered / injected structures from passing.
    positions = [text.index(h) for h in REQUIRED_HEADERS] + [text.index(SAFETY_FOOTER)]
    if positions != sorted(positions):
        raise ValueError("Sections out of order")


def validate_numbers_preserved(input_text: str, output_text: str) -> None:
    """Every digit group in the input must survive in the output.

    Catches dropped doses, deadlines and quantities ("50mg" -> "50 mg" is
    fine, digits are compared; a missing "180" or "7" fails closed).
    """
    in_nums = set(re.findall(r"\d+", input_text))
    out_nums = set(re.findall(r"\d+", output_text))
    missing = sorted(in_nums - out_nums, key=int)
    if missing:
        raise ValueError(f"Dropped numbers from input: {', '.join(missing)}")
