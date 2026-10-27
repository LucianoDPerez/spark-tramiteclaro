"""Language profiles: headers, footer, voice, OCR, negation and UI copy.

Single place to add a language. Everything downstream (prompt, validator,
TTS, OCR, UI) reads from here, so no language literals leak into other files.
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class LanguageProfile:
    code: str
    label: str
    headers: tuple[str, str, str]
    footer: str
    tts_voice: str
    ocr_lang: str
    negation_markers: tuple[str, ...]
    cjk: bool
    system_prompt: str
    user_prefix: str
    ui: dict[str, str] = field(default_factory=dict)


_SPANISH = LanguageProfile(
    code="es",
    label="Español",
    headers=("VERSIÓN SIMPLE:", "PASOS A SEGUIR:", "QUÉ LLEVAR / QUÉ PREGUNTAR:"),
    footer=(
        "Esto es una ayuda explicativa, no reemplaza al profesional. "
        "Si es urgente, buscá atención humana."
    ),
    tts_voice="Paulina",
    ocr_lang="spa",
    negation_markers=(
        "no", "nunca", "jamas", "sin", "ni", "nada", "ningun", "ninguna",
        "ninguno", "tampoco", "evite", "evitar", "prohibido",
    ),
    cjk=False,
    system_prompt="""Sos un asistente de accesibilidad. Tu tarea es explicar textos oficiales o de salud en español simple.
Reglas estrictas:
1. No das diagnósticos ni indicas dosis ni tratamientos. Solo explicas lo que dice el texto.
2. Devolvé SIEMPRE estas 3 partes con estos títulos exactos:
VERSIÓN SIMPLE:
PASOS A SEGUIR:
QUÉ LLEVAR / QUÉ PREGUNTAR:
3. Usá frases cortas, sin jerga. Si algo es ambiguo, decilo.
4. Nunca cambies el sentido de una negación ni de una prohibición: si el texto dice "no", "sin" o "nunca", tu explicación lo tiene que decir igual.
5. Copiá los números, fechas y plazos exactamente como aparecen en el texto.
6. Al final agregá una línea: "Esto es una ayuda explicativa, no reemplaza al profesional. Si es urgente, buscá atención humana."
7. No inventes datos que no estén en el texto. Si falta info, pedila.
""",
    user_prefix="Explicá este texto:",
    ui={
        "title": "TramiteClaro local",
        "caption": "HER Hack-Astron #7 · Spark-X2.6-4B 100% local · No sale de tu máquina",
        "lang_label": "Idioma",
        "big_text": "🔍 Texto grande",
        "photo_section": "Foto del papel",
        "photo_upload": "Subí una foto del texto (se lee en tu máquina, sin subir nada)",
        "photo_button": "Leer foto",
        "photo_working": "Leyendo la imagen en local...",
        "photo_ok": "Texto leído de la imagen.",
        "text_label": "Pegá el texto oficial o indicación de salud:",
        "text_placeholder": "Ej: requisitos para un turno, indicación de farmacia, cartel de defensa civil...",
        "temp_label": "Creatividad (temperature)",
        "advanced": "Opciones avanzadas",
        "explain_button": "Explicar en simple",
        "listen_button": "Escuchar en voz alta",
        "need_text": "Pegá un texto primero.",
        "working": "Spark-X2.6-4B explicando en local...",
        "done": "Listo",
        "result_title": "Resultado",
        "audio_working": "Generando audio en local...",
        "cache_hit": "Cache hit · idempotente",
        "local": "local",
        "disclaimer": "Ayuda explicativa, no reemplaza al profesional. No pegues datos personales.",
        "error_server": "¿llama-server en :8080?",
        "error_unexpected": "Error inesperado. Revisá el server local.",
    },
)

_ENGLISH = LanguageProfile(
    code="en",
    label="English",
    headers=("SIMPLE VERSION:", "STEPS TO FOLLOW:", "WHAT TO BRING / WHAT TO ASK:"),
    footer=(
        "This is an explanatory aid, it does not replace a professional. "
        "If it is urgent, seek human help."
    ),
    tts_voice="Samantha",
    ocr_lang="eng",
    negation_markers=(
        "no", "not", "never", "without", "none", "nothing", "cannot",
        "dont", "prohibited", "avoid", "except",
    ),
    cjk=False,
    system_prompt="""You are an accessibility assistant. Your job is to explain official or health texts in plain English.
Strict rules:
1. You do not diagnose, prescribe or give dosages. You only explain what the text says.
2. Always answer with these 3 parts using these exact headings:
SIMPLE VERSION:
STEPS TO FOLLOW:
WHAT TO BRING / WHAT TO ASK:
3. Use short sentences, no jargon. If something is ambiguous, say so.
4. Never invert a negation or a prohibition: if the text says "no", "without" or "never", your explanation must say it too.
5. Copy numbers, dates and deadlines exactly as they appear in the text.
6. End with one line: "This is an explanatory aid, it does not replace a professional. If it is urgent, seek human help."
7. Do not invent facts that are not in the text. If information is missing, ask for it.
""",
    user_prefix="Explain this text:",
    ui={
        "title": "TramiteClaro local",
        "caption": "HER Hack-Astron #7 · Spark-X2.6-4B 100% local · Nothing leaves your machine",
        "lang_label": "Language",
        "big_text": "🔍 Larger text",
        "photo_section": "Photo of the paper",
        "photo_upload": "Upload a photo of the text (read on your machine, nothing uploaded)",
        "photo_button": "Read photo",
        "photo_working": "Reading the image locally...",
        "photo_ok": "Text read from the image.",
        "text_label": "Paste the official or health text:",
        "text_placeholder": "E.g. appointment requirements, pharmacy instructions, civil defense notice...",
        "temp_label": "Creativity (temperature)",
        "advanced": "Advanced options",
        "explain_button": "Explain in plain language",
        "listen_button": "Listen aloud",
        "need_text": "Paste a text first.",
        "working": "Spark-X2.6-4B explaining locally...",
        "done": "Done",
        "result_title": "Result",
        "audio_working": "Generating audio locally...",
        "cache_hit": "Cache hit · idempotent",
        "local": "local",
        "disclaimer": "Explanatory aid, does not replace a professional. Do not paste personal data.",
        "error_server": "Is llama-server on :8080?",
        "error_unexpected": "Unexpected error. Check the local server.",
    },
)

_CHINESE = LanguageProfile(
    code="zh",
    label="中文",
    headers=("简明版本：", "办理步骤：", "需要携带 / 需要询问："),
    footer="这是解释性帮助，不能替代专业人员。如有紧急情况，请寻求人工帮助。",
    tts_voice="Tingting",
    ocr_lang="chi_sim",
    negation_markers=("不", "未", "無", "无", "勿", "禁止", "免", "停"),
    cjk=True,
    system_prompt="""你是一个无障碍阅读助手。你的任务是用简明中文解释官方通知或健康材料。
严格规则：
1. 不做诊断，不给出剂量或治疗方案。只解释原文说了什么。
2. 始终使用以下三个固定标题回答：
简明版本：
办理步骤：
需要携带 / 需要询问：
3. 使用短句，避免专业术语。如果原文有歧义，请说明。
4. 绝不改变否定或禁止的意思：如果原文说"不"、"未"、"禁止"、"勿"，你的解释也必须保留。
5. 数字、日期和期限必须与原文完全一致地照抄。
6. 最后加一行："这是解释性帮助，不能替代专业人员。如有紧急情况，请寻求人工帮助。"
7. 不要编造原文没有的信息。如缺少信息，请提出。
""",
    user_prefix="请解释这段文字：",
    ui={
        "title": "TramiteClaro 本地版",
        "caption": "HER Hack-Astron #7 · Spark-X2.6-4B 完全本地运行 · 数据不出你的电脑",
        "lang_label": "语言",
        "big_text": "🔍 大字体",
        "photo_section": "拍摄纸张照片",
        "photo_upload": "上传文字照片（在本机识别，不会上传）",
        "photo_button": "识别照片",
        "photo_working": "正在本地识别图片……",
        "photo_ok": "已从图片读取文字。",
        "text_label": "粘贴官方通知或健康材料：",
        "text_placeholder": "例如：办事所需材料、药店用药说明、民防通告……",
        "temp_label": "创造度（temperature）",
        "advanced": "高级选项",
        "explain_button": "用简明语言解释",
        "listen_button": "朗读",
        "need_text": "请先粘贴文本。",
        "working": "Spark-X2.6-4B 正在本地解释……",
        "done": "完成",
        "result_title": "结果",
        "audio_working": "正在本地生成音频……",
        "cache_hit": "缓存命中 · 幂等",
        "local": "本地",
        "disclaimer": "解释性帮助，不能替代专业人员。请勿粘贴个人隐私数据。",
        "error_server": "llama-server 是否在 :8080 运行？",
        "error_unexpected": "发生意外错误，请检查本地服务。",
    },
)

PROFILES: dict[str, LanguageProfile] = {p.code: p for p in (_SPANISH, _ENGLISH, _CHINESE)}
DEFAULT_LANGUAGE = "es"


def get_profile(code: str) -> LanguageProfile:
    try:
        return PROFILES[code]
    except KeyError:
        raise ValueError(f"Unsupported language: {code}") from None
