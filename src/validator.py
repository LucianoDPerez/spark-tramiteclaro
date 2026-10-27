"""Output validator: fail-closed checks (structure, numbers, negations)."""
from __future__ import annotations

import re
import unicodedata

from .languages import LanguageProfile


def _cleaned(output: str) -> str:
    # Model sometimes wraps headers in markdown bold (**...**). Strip it.
    return output.replace("*", "")


def _strip_accents(text: str) -> str:
    return "".join(
        c for c in unicodedata.normalize("NFD", text)
        if unicodedata.category(c) != "Mn"
    )


def validate_output(output: str, profile: LanguageProfile) -> None:
    """Raise ValueError if output breaks the 3-section + footer contract."""
    if not output or not output.strip():
        raise ValueError("Empty model output")
    text = _cleaned(output)
    missing = [h for h in profile.headers if h not in text]
    if missing:
        raise ValueError(f"Missing sections: {', '.join(missing)}")
    # A duplicated header means the model restarted the template mid-answer.
    duplicated = [h for h in profile.headers if text.count(h) > 1]
    if duplicated:
        raise ValueError(f"Duplicated sections: {', '.join(duplicated)}")
    if profile.footer not in text:
        raise ValueError("Missing safety footer")
    # Order matters: prevents reordered / injected structures from passing.
    positions = [text.index(h) for h in profile.headers] + [text.index(profile.footer)]
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


def count_negations(text: str, profile: LanguageProfile) -> int:
    normalized = _strip_accents(text).lower()
    if profile.cjk:
        # No word boundaries in CJK: count marker occurrences directly.
        return sum(normalized.count(m) for m in profile.negation_markers)
    pattern = r"\b(" + "|".join(re.escape(m) for m in profile.negation_markers) + r")\b"
    return len(re.findall(pattern, normalized))


def validate_negations_preserved(
    input_text: str,
    output_text: str,
    profile: LanguageProfile,
    min_ratio: float,
) -> None:
    """A dropped negation inverts medical/bureaucratic meaning. Fail closed."""
    in_count = count_negations(input_text, profile)
    if in_count == 0:
        return
    # The fixed safety footer contains a negation ("no reemplaza" / "does not
    # replace" / "不能替代"). Counting it would mask a dropped negation in the
    # actual explanation, so the footer is excluded from the output side.
    body = _cleaned(output_text).replace(profile.footer, "")
    out_count = count_negations(body, profile)
    required = int(in_count * min_ratio)
    if out_count < required:
        raise ValueError(
            f"Negation may be inverted: input has {in_count}, output has {out_count}"
        )
