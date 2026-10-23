"""Record real demo video (no fakes): fill ejemplo 1, click, wait for Spark output."""
from playwright.sync_api import sync_playwright

URL = "http://localhost:8501"
TEXTO = "Tomar 1 comprimido de 50mg cada 12 horas con las comidas durante 7 días. No interrumpir el tratamiento aunque mejoren los síntomas. Conservar en lugar fresco y seco. Ante mareos o sarpullido consultar al médico."

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    ctx = browser.new_context(viewport={"width": 1280, "height": 800}, record_video_dir="docs/")
    page = ctx.new_page()
    page.goto(URL)
    page.wait_for_selector("textarea", timeout=30000)
    page.fill("textarea", TEXTO)
    page.wait_for_timeout(1500)
    page.get_by_role("button", name="Explicar en simple").click()
    # Wait for real model output (local Q4_K_M ~30-45s) + buffer
    page.wait_for_selector("text=VERSIÓN SIMPLE", timeout=180000)
    page.wait_for_timeout(3000)
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(2000)
    ctx.close()
    browser.close()
print("done - check docs/ video")
