"""CLI thin wrapper (kept for reproducibility). Usage: python3 simplificar.py <file>"""
import sys
from src.usecase import SimplifyTextUseCase, ValidationError
from src.domain import SimplifyRequest
from src.llm_client import LLMError

def main() -> int:
    if len(sys.argv) > 1:
        texto = open(sys.argv[1], encoding="utf-8").read()
    else:
        texto = input("Pega el texto oficial:\n")
    try:
        res = SimplifyTextUseCase().execute(SimplifyRequest(text=texto))
        print(res.output)
        return 0
    except (ValidationError, LLMError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
