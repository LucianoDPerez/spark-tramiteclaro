"""Unit tests without model (DIP: fake LLM port). Run: python3 -m unittest -v"""
import unittest
from src.domain import SimplifyRequest, normalize
from src.usecase import SimplifyTextUseCase, ValidationError
from src.cache import InMemoryCache
from src.ratelimit import RateLimiter


class FakeLLM:
    def __init__(self):
        self.calls = 0
    def complete(self, text: str, temperature: float) -> str:
        self.calls += 1
        return "VERSIÓN SIMPLE:\nHola"


class UseCaseTest(unittest.TestCase):
    def test_normalize_dedupes(self):
        self.assertEqual(normalize("  hola   mundo "), "hola mundo")

    def test_idempotent_same_input_hits_cache(self):
        fake = FakeLLM()
        uc = SimplifyTextUseCase(llm=fake, cache=InMemoryCache(), limiter=RateLimiter(0))
        req = SimplifyRequest(text="Este es un texto oficial de prueba con más de veinte caracteres.")
        r1 = uc.execute(req)
        r2 = uc.execute(req)
        self.assertFalse(r1.cached)
        self.assertTrue(r2.cached)
        self.assertEqual(fake.calls, 1)

    def test_validation_rejects_short(self):
        uc = SimplifyTextUseCase(llm=FakeLLM(), cache=InMemoryCache(), limiter=RateLimiter(0))
        with self.assertRaises(ValidationError):
            uc.execute(SimplifyRequest(text="corto"))


if __name__ == "__main__":
    unittest.main()
