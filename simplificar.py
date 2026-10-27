"""CLI thin wrapper (kept for reproducibility). Usage: python3 simplificar.py <file> [lang]"""
import sys
from src.usecase import SimplifyTextUseCase, ValidationError
from src.domain import SimplifyRequest
from src.llm_client import LLMError
from src.languages import PROFILES
from src.locale_detect import detect_language

def main() -> int:
    if len(sys.argv) > 1:
        texto = open(sys.argv[1], encoding="utf-8").read()
    else:
        texto = input("Pega el texto oficial:\n")
    lang = sys.argv[2] if len(sys.argv) > 2 else detect_language()
    if lang not in PROFILES:
        print(f"Error: idioma no soportado '{lang}'. Usa: {', '.join(PROFILES)}", file=sys.stderr)
        return 1
    try:
        res = SimplifyTextUseCase().execute(
            SimplifyRequest(text=texto, language=lang)
        )
        print(res.output)
        return 0
    except (ValidationError, LLMError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
