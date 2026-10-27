"""Fact-retention evaluation dataset (synthetic, no personal data).

Each case declares the facts a correct explanation must keep. Facts are
checked as substrings after normalization (case/accent/whitespace), which is
a conservative check: it proves presence, never semantic equivalence.
"""

CASES = [
    {
        "id": "es-turno",
        "language": "es",
        "text": (
            "Deberá presentarse con 30 minutos de antelación al horario asignado, "
            "con DNI original, credencial de obra social y orden médica autorizada. "
            "En caso de estudios con contraste deberá concurrir con 8 hs de ayuno. "
            "La tolerancia máxima es de 10 minutos."
        ),
        "facts": ["30 minutos", "dni", "obra social", "orden medica", "8", "10 minutos"],
    },
    {
        "id": "es-farmacia",
        "language": "es",
        "text": (
            "Tomar 1 comprimido de 50mg cada 12 horas con las comidas durante 7 días. "
            "No interrumpir el tratamiento aunque mejoren los síntomas. "
            "Conservar en lugar fresco y seco. Ante mareos o sarpullido consultar al médico."
        ),
        "facts": ["1 comprimido", "50", "12 horas", "7", "no interrumpir", "mareos"],
    },
    {
        "id": "es-alerta",
        "language": "es",
        "text": (
            "Ante alerta amarilla por tormentas, evite circular por calles anegadas, "
            "desconecte artefactos eléctricos en planta baja y prepare documentación "
            "en bolsa estanca. En caso de evacuación siga las indicaciones del personal."
        ),
        "facts": ["alerta amarilla", "calles anegadas", "artefactos electricos", "bolsa estanca"],
    },
    {
        "id": "en-clinic",
        "language": "en",
        "text": (
            "Patients must arrive 30 minutes before the appointment with original ID "
            "and insurance card. Fasting for 8 hours is required for contrast studies. "
            "Late arrival beyond 10 minutes will not be accepted."
        ),
        "facts": ["30 minutes", "id", "insurance card", "8 hours", "10 minutes", "not"],
    },
    {
        "id": "en-medication",
        "language": "en",
        "text": (
            "Take 1 tablet of 50mg every 12 hours with meals for 7 days. "
            "Do not stop the treatment even if symptoms improve. "
            "Store in a cool dry place. Consult a doctor if dizziness or rash appears."
        ),
        "facts": ["1 tablet", "50", "12 hours", "7 days", "do not", "dizziness"],
    },
    {
        "id": "en-benefits",
        "language": "en",
        "text": (
            "Your benefits will stop without further notice if the renewal form and "
            "the phone interview are missed. The deadline is 45 days from this letter. "
            "Call 555-0142 to reschedule."
        ),
        "facts": ["without", "45 days", "555-0142", "interview"],
    },
    {
        "id": "zh-预约",
        "language": "zh",
        "text": (
            "请于预约时间前30分钟到达，携带身份证原件、医保卡和已授权的医生处方。"
            "进行增强检查需空腹8小时。迟到超过10分钟不予受理。"
        ),
        "facts": ["30", "身份证", "医保卡", "处方", "8", "10"],
    },
    {
        "id": "zh-用药",
        "language": "zh",
        "text": (
            "每次服用1片50毫克，每12小时一次，随餐服用，连续7天。"
            "即使症状好转也不要中断治疗。请置于阴凉干燥处保存。"
        ),
        "facts": ["1", "50", "12", "7", "不要中断", "阴凉"],
    },
    {
        "id": "zh-通知",
        "language": "zh",
        "text": (
            "社区手作课共有15个名额，材料费暂定100元，最终费用以开课公告为准。"
            "目前不接受报名，也不收取订金。"
        ),
        "facts": ["15", "100", "不接受报名", "订金"],
    },
]
