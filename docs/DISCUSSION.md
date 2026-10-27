# [HER Hack-Astron #7] [Open Source AI for Good] TramiteClaro local - plain-language access with Spark-X2.6-4B

## Project name and track
Project name: TramiteClaro local
Track: Accessibility + Health and well-being (plain-language explanation of official and health texts, offline-first)

## Who this helps and what problem it solves
Target users: older adults and low-literacy users in Argentina/LATAM who struggle with bureaucratic and health instructions (appointments, prescriptions, civil-defense alerts).
Concrete scenario and problem: official texts are long, jargon-heavy, and cause missed appointments, medication errors, or unsafe behavior in floods. Users will not paste sensitive documents into cloud chatbots for privacy reasons.
Expected public benefit: a 100% local explainer that returns VERSIÓN SIMPLE + PASOS A SEGUIR + QUÉ LLEVAR / QUÉ PREGUNTAR, with a safety footer. No data leaves the device.

## How Spark-X2.6-4B is used
Model source and revision: `XHToken Spark-X2.6-4B-GGUF`, file `Spark-X2.6-4B-Q4_K_M.gguf`, snapshot revision `fe31f8d64890302cc3a1d365d700357b4b75ba77` (local HF cache `models--XHToken--Spark-X2.6-4B-GGUF`).
The model's role in the application: sole generator. It rewrites the input into the 3 fixed sections + safety line. No other LLM is used. App logic only validates, caches, and rate-limits.
Other models, tools, or services used, if any: none for inference and none for language. Speech and OCR are non-LLM local tools: offline macOS `say` for audio (`Paulina` / `Samantha` / `Tingting`) and local `tesseract` for photo-to-text. App stack: Python + Streamlit UI + `requests` to local llama-server. No cloud calls.

### Multilingual use (Spanish / English / Chinese)
The model card lists only `en` and `zh`, yet the same revision also produces correct Spanish. All three locales use the same code path: one `LanguageProfile` per language defines headers, footer, system prompt, TTS voice, OCR language and negation markers.

Measured today on the same local Q4_K_M server, one real medication text per language, all accepted by the fail-closed gates:

| Locale | Raw latency | Structure | Numbers kept | Negation kept |
| --- | --- | --- | --- | --- |
| es | 22.4 s | pass | pass | pass |
| en | 20.1 s | pass | pass | pass |
| zh | 15.7 s | pass | pass | pass |

This is a 1-sample-per-language smoke test, not a benchmark. The Spanish result is a transfer observation: `es` is not a declared language of the model card.

## Demo (illustrated walkthrough with Streamlit screenshots below)
Video link / embedded screenshots: 4 Streamlit screenshots attached below (empty -> filled -> running -> output). UI flow: input box -> Explicar en simple -> 3 sections. Below are 3 real end-to-end runs via `simplificar.py` on local server.

Beyond the text box, the app has two extra local paths, both without cloud:
- **Escuchar en voz alta** — the finished explanation is spoken by an offline macOS voice (`Paulina` es, `Samantha` en, `Tingting` zh), then played in the browser. For older adults and low-literacy users, reading is the barrier, not just the vocabulary.
- **Foto del papel** — upload a photo of the paper; local `tesseract` (bundled `spa`/`eng`/`chi_sim`) extracts the text into the input box. Verified on a clean 34px sample: `Deberá presentarse con 30 minutos de antelación. En caso de estudios con contraste: 8 horas de ayuno. No interrumpir el tratamiento.` came back verbatim.
- **Language selector** — defaults to the detected OS locale (`src/locale_detect.py`), switchable to Español / English / 中文 at any time; the whole UI is translated.

New screenshots for this revision: `docs/demo-es.png` (Spanish output + 48 s audio player), `docs/demo-zh.png` (Chinese output), `docs/demo-photo.png` (photo -> OCR -> explanation). All three are real local runs. `docs/demo-walkthrough.mp4` (36 s) is a montage of these real captures with real offline narration (macOS `say`), assembled with ffmpeg; each frame is an unedited local run.

Example input 1 (medical appointment, ES real):
Deberá presentarse con 30 minutos de antelación al horario asignado, con DNI original, credencial de obra social y orden médica autorizada. En caso de estudios con contraste deberá concurrir con 8 hs de ayuno. La tolerancia máxima es de 10 minutos.
Application workflow and actual output (verbatim, 32624ms):
```
VERSIÓN SIMPLE:
Tienes que llegar 30 minutos antes del horario. Lleva tu DNI original, tu credencial de la obra social y tu orden médica. Si estás haciendo estudios con contraste, debes ir 8 horas antes de comer. La tolerancia máxima es de 10 minutos.
PASOS A SEGUIR:
1. Llega 30 minutos antes del horario.
2. Lleva tu DNI original.
3. Lleva tu credencial de la obra social.
4. Lleva tu orden médica.
5. Si haces estudios con contraste, haz 8 horas de ayuno.
6. No llegues más de 10 minutos después del horario.
QUÉ LLEVAR / QUÉ PREGUNTAR:
- Lleva: DNI original, credencial de la obra social, orden médica.
- Si no tienes tu orden médica o tu credencial de la obra social, pregunta dónde la obtienes.
Esto es una ayuda explicativa, no reemplaza al profesional. Si es urgente, buscá atención humana.
```

Example input 2 (pharmacy, ES real, 41199ms):
Tomar 1 comprimido de 50mg cada 12 horas con las comidas durante 7 días. No interrumpir el tratamiento aunque mejoren los síntomas. Conservar en lugar fresco y seco. Ante mareos o sarpullido consultar al médico.
Actual output (verbatim):
```
VERSIÓN SIMPLE:
- Tomar 1 comprimido de 50 mg cada 12 horas, con las comidas.
- Tomar durante 7 días.
- No interrumpir el tratamiento, aunque los síntomas mejoren.
- Guardar el medicamento en un lugar fresco y seco.
- Si se tienen mareos o sarpullido, consultar al médico.
PASOS A SEGUIR:
1. Tomar 1 comprimido de 50 mg cada 12 horas.
2. Tomar el comprimido con las comidas.
3. Tomar durante 7 días.
4. No interrumpir el tratamiento, aunque los síntomas mejoren.
5. Guardar el medicamento en un lugar fresco y seco.
6. Si se tienen mareos o sarpullido, consultar al médico.
QUÉ LLEVAR / QUÉ PREGUNTAR:
- Llevar el medicamento guardado en un lugar fresco y seco.
- Llevar el comprimido de 50 mg.
- Llevar el calendario para recordar los 7 días.
- Llevar el informe del médico si se tienen mareos o sarpullido.
- Llevar el teléfono para contactar al médico si se tienen mareos o sarpullido.
Esto es una ayuda explicativa, no reemplaza al profesional. Si es urgente, buscá atención humana.
```

Example input 3 (flood alert, ES real, 34179ms):
Ante alerta amarilla por tormentas, evite circular por calles anegadas, desconecte artefactos eléctricos en planta baja y prepare documentación en bolsa estanca. En caso de evacuación siga las indicaciones del personal.
Actual output (verbatim):
```
**VERSIÓN SIMPLE:**
Si hay tormentas, no circules por calles que estén inundadas. Desconecta los aparatos eléctricos que están en la planta baja. Guarda tu documentación en una bolsa cerrada. Si te piden que te evacues, sigue las instrucciones del personal.
**PASOS A SEGUIR:**
1. No uses carreteras o calles anegadas.
2. Desconecta aparatos eléctricos de la planta baja.
3. Guarda tu documentación en una bolsa cerrada.
4. Si te piden evacuación, sigue las indicaciones del personal.
**QUÉ LLEVAR / QUÉ PREGUNTAR:**
- Lleva una bolsa cerrada para guardar documentación.
- Pregunta al personal si hay que evacuar y qué hacer.
Esto es una ayuda explicativa, no reemplaza al profesional. Si es urgente, buscá atención humana.
```

## How to reproduce
Code repository or runnable example, if available: https://github.com/LucianoDPerez/spark-tramiteclaro (`src/config.py`, `src/domain.py`, `src/usecase.py`, `src/llm_client.py`, `src/cache.py`, `src/ratelimit.py`, `app.py`, `simplificar.py`, `test_usecase.py`).
Setup and run instructions:
1. Run llama-server: `llama-server -m /Users/luchop/.cache/huggingface/hub/models--XHToken--Spark-X2.6-4B-GGUF/snapshots/fe31f8d64890302cc3a1d365d700357b4b75ba77/Spark-X2.6-4B-Q4_K_M.gguf -c 16384 -ngl 99 --flash-attn on --threads 10 --threads-batch 10 --batch-size 1024 --ubatch-size 512 --port 8080 --host 0.0.0.0 --alias spark2.6-4B --temp 0.2 --top-p 0.95 --top-k 20 --min-p 0.0 --presence-penalty 0.0 --repeat-penalty 1.05 --parallel 1 --jinja --cont-batching`
2. `pip install -r requirements.txt` (streamlit, requests, pillow). OCR needs `tesseract` installed; language data (`spa`, `eng`, `chi_sim`) is bundled in `models/tessdata/`.
3. `python3 -m unittest -v` (25 tests, no model needed: structure, numbers, negations, per-language coverage, locale detection, adapter guards)
4. `python3 -m eval.run_eval` (fact-retention table, needs the model) or `python3 -m eval.run_eval --lang zh`
5. `python3 -c "from src.usecase import SimplifyTextUseCase; from src.domain import SimplifyRequest; print(SimplifyTextUseCase().execute(SimplifyRequest(text=open('ejemplos.txt').read())).output)"` or `streamlit run app.py`
Runtime and versions: llama.cpp `llama_server` (build b11669-620d2225c per fingerprint), Python 3.14, streamlit, requests. OpenAI-compatible endpoint `http://localhost:8080/v1/chat/completions`, model id `spark2.6-4B`.
Hardware and precision/quantization: Mac, threads 10, GGUF Q4_K_M (4.44B params, n_ctx 16384 per /v1/models), flash-attn on.
Key prompts and inference settings: one system prompt per locale in `src/languages.py` (3 fixed sections + safety footer, no diagnosis, explicit "never invert a negation", "copy numbers exactly"). `temperature 0.2, top_p 0.95, max_tokens 1200, chat_template_kwargs {enable_thinking: False}` (thinking disabled because default high fills 1024 tokens with reasoning only). `n_ctx 16384`. The UI language defaults to the detected OS locale (`src/locale_detect.py`) and can be switched at any time.

## Fact-retention evaluation
Harness: `eval/run_eval.py` over 9 synthetic cases (3 per language), each declaring the facts a correct explanation must keep. Facts are matched as substrings after case/accent normalization, which is conservative: it proves presence, never semantic equivalence. Every case runs through the full fail-closed pipeline.

**Result: 39/42 facts retained, 8/9 cases accepted, median latency 45.9 s** (local Q4_K_M, single slot, machine also running the UI).

| Case | Lang | Status | Facts kept |
| --- | --- | --- | --- |
| es-turno | es | ok | 6/6 |
| es-farmacia | es | ok | 6/6 |
| es-alerta | es | ok | **1/4** |
| en-clinic | en | ok | 6/6 |
| en-medication | en | ok | 6/6 |
| en-benefits | en | ok | 4/4 |
| zh-预约 | zh | ok | 6/6 |
| zh-用药 | zh | **rejected** | — (`Dropped numbers from input: 50`) |
| zh-通知 | zh | ok | 4/4 |

### What the failures actually were
- **es-alerta, real losses:** the output never says "alerta amarilla" (the severity level disappears, leaving just "si hay tormentas"), and turns "bolsa estanca" (watertight) into "bolsa cerrada" (closed). In a flood, watertight is the whole point.
- **es-alerta, real drift in the steps:** step 2 says "Cierra los aparatos eléctricos" instead of "desconecta", and "pregunta al personal" became "pregúntate", turning an external instruction into self-reflection.
- **es-alerta, false negative of the method:** "artefactos eléctricos" → "aparatos eléctricos" is a synonym, not a loss. Substring matching cannot tell the difference; this is a limitation of the measurement, not of the model.
- **zh-用药, correct rejection:** the model dropped the "50" from "50毫克". The numbers gate rejected the output and nothing was shown. Same input on another run passed, so this is intermittent — which is exactly why the gate exists.
- **The worst one, found while recording the photo demo:** on the appointment notice, the model merged two separate instructions and wrote *"El tiempo máximo de ayuno es de 10 minutos"* and *"No pasar más de 10 minutos de ayuno"*. The 10 minutes are the lateness tolerance, not the fasting window (8 hours). Both numbers are present, so the numbers gate cannot catch it: **preserving a number is not the same as attaching it to the right fact.** This is reproducible on that input and is the strongest argument for the human-review footer. A second reproducible failure on the same input: the model restarted the template mid-answer and emitted the three headings twice with empty bodies. A duplicate-header gate now rejects that case (`Duplicated sections`), and a unit test covers it.

This is a development-set check on synthetic texts, not a blind benchmark, and there is no human user study.
## Fail-closed validation gates
Three deterministic gates run before any output reaches the screen or the cache. Rejected output is never cached, so a retry hits the model again instead of replaying a bad answer.

| Gate | What it catches | Implementation |
| --- | --- | --- |
| Structure | missing or reordered sections, **duplicated sections**, missing safety footer | `validate_output` |
| Numbers | dropped dose, deadline or quantity (`50mg`, `180 days`) | `validate_numbers_preserved` |
| Negation | a prohibition rewritten as a positive instruction | `validate_negations_preserved` |

The negation gate excludes the fixed safety footer from counting, because the footer itself contains a negation ("no reemplaza") and would otherwise mask a dropped one. This was found by a failing unit test, not by inspection.

Verified: a tampered dose (`cada 12 horas` -> `cada 24 horas`) is rejected on `Dropped numbers from input: 12`; an inverted prohibition is rejected on `Negation may be inverted`.

## Results and limitations
Observed results and how they were evaluated: 3/3 real local runs completed with correct 3-section structure and safety footer. Unit tests **25/25** pass with no model: structure (missing section, bold headers, order, duplicated sections), numbers preserved/dropped, negations preserved/dropped, accent-insensitive markers, per-language coverage (es/en/zh), locale detection, and adapter guards (TTS/OCR reject bad input). The three fail-closed gates (structure, numbers, negation) reject before caching, so a retry hits the model again instead of replaying a bad answer. All 3 published real runs pass all gates. Idempotency verified: second identical call served from cache (0ms). Latency 32-41s on local Mac Q4_K_M.
Failure cases and current limitations:
- EX1 ayuno phrasing: output says "debes ir 8 horas antes de comer" (ambiguous) alongside correct "haz 8 horas de ayuno". Fasting instruction must be reviewed by human; prototype does not replace staff. Validator checks structure and facts, not clinical wording.
- Short inputs are often copied instead of paraphrased: on a one-sentence medication text the model repeated the source nearly verbatim (es/en), so the "simplification" gain is small there. Chinese simplified better. The prompt was kept unchanged from the 3 published runs on purpose, to preserve reproducibility of those outputs.
- Chinese medication case: in one run the model dropped the "50" of "50毫克". The numbers gate rejected the output (correctly) and nothing was shown; the user must retry. This is the gate working, but it means roughly one in three hard cases needs a retry.
- The negation gate is only a counter: in Latin languages it detects a dropped negation reasonably well, but in Chinese it counts characters like 不, so it catches mass loss, not a single subtly inverted clause.
- Photo input depends on image quality: a clean 34px scan reads perfectly, a small/thin font misreads words. OCR is not evaluated on real photographed documents.
- Adversarial prompt-injection is contained only at the structure level: unstructured model output is rejected and never cached; semantic jailbreaks beyond structure are not covered.
- Long legal texts over 4000 chars are rejected by validation (by design, single 16k slot).
- Thinking disabled for latency; complex multi-step reasoning quality not evaluated.
- No PII handling beyond warning; do not paste personal data.

## Contributors and disclosure
Individual: Luciano David Perez (https://github.com/LucianoDPerez)
AI-assisted development disclosure: scaffolding and prompt iteration assisted by AI coding agent; all model outputs above are verbatim local runs, no fabricated outputs.
Data sources and authorization, if applicable: hand-written generic Spanish examples (no personal data, no copyrighted texts).
