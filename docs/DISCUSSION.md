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
Other models, tools, or services used, if any: none for inference. App stack: Python + Streamlit UI + `requests` to local llama-server. No cloud calls.

## Demo (illustrated walkthrough - no video yet, screenshots from Streamlit to add)
Video link / embedded screenshots: Streamlit `app.py` screenshots to be attached (UI: input box -> Explicar en simple -> 3 sections). Below are 3 real end-to-end runs via `simplificar.py` on local server.

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
2. `pip install -r requirements.txt` (streamlit, requests)
3. `python3 -m unittest -v` (3 tests, no model needed)
4. `python3 -c "from src.usecase import SimplifyTextUseCase; from src.domain import SimplifyRequest; print(SimplifyTextUseCase().execute(SimplifyRequest(text=open('ejemplos.txt').read())).output)"` or `streamlit run app.py`
Runtime and versions: llama.cpp `llama_server` (build b11669-620d2225c per fingerprint), Python 3.14, streamlit, requests. OpenAI-compatible endpoint `http://localhost:8080/v1/chat/completions`, model id `spark2.6-4B`.
Hardware and precision/quantization: Mac, threads 10, GGUF Q4_K_M (4.44B params, n_ctx 16384 per /v1/models), flash-attn on.
Key prompts and inference settings: SYSTEM_PROMPT in `src/prompts.py:1` (Spanish, 3 fixed sections + safety footer, no diagnosis). `temperature 0.2, top_p 0.95, max_tokens 1200, chat_template_kwargs {enable_thinking: False}` (thinking disabled because default high fills 1024 tokens with reasoning only). `n_ctx 16384`.

## Results and limitations
Observed results and how they were evaluated: 3/3 real local runs completed with correct 3-section structure and safety footer. Unit tests 3/3 pass (normalize, idempotency cache, validation). Idempotency verified: second identical call served from cache (0ms). Latency 32-41s on local Mac Q4_K_M.
Failure cases and current limitations:
- EX1 ayuno phrasing: output says "debes ir 8 horas antes de comer" (ambiguous) alongside correct "haz 8 horas de ayuno". Fasting instruction must be reviewed by human; prototype does not replace staff.
- Long legal texts over 4000 chars are rejected by validation (by design, single 16k slot).
- Thinking disabled for latency; complex multi-step reasoning quality not evaluated.
- No PII handling beyond warning; do not paste personal data.

## Contributors and disclosure
Individual: Luciano David Perez (https://github.com/LucianoDPerez)
AI-assisted development disclosure: scaffolding and prompt iteration assisted by AI coding agent; all model outputs above are verbatim local runs, no fabricated outputs.
Data sources and authorization, if applicable: hand-written generic Spanish examples (no personal data, no copyrighted texts).
