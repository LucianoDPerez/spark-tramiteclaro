"""Streamlit UI - thin layer over SimplifyTextUseCase. No business logic here."""
import streamlit as st
import streamlit.components.v1 as components
from src.usecase import SimplifyTextUseCase, ValidationError
from src.domain import SimplifyRequest
from src.llm_client import LLMError
from src.languages import PROFILES, get_profile
from src.locale_detect import detect_language
from src.tts import MacSayTTS, TTSError
from src.ocr import TesseractOCR, OCRError

@st.cache_resource
def get_usecase() -> SimplifyTextUseCase:
    return SimplifyTextUseCase()

@st.cache_resource
def get_tts() -> MacSayTTS:
    return MacSayTTS()

@st.cache_resource
def get_ocr() -> TesseractOCR:
    return TesseractOCR()

st.set_page_config(
    page_title="TramiteClaro local - Spark-X2.6-4B",
    page_icon="🩺",
    layout="centered",
)

# Hide Streamlit's Deploy button (testid-verified). The ⋮ menu with
# Settings (light/dark) stays untouched.
st.markdown(
    """
    <style>
    button[data-testid="stBaseButton-header"] { display: none; }
    </style>
    """,
    unsafe_allow_html=True,
)

# Language chosen in the previous run drives this run's copy (selectbox reruns).
lang_code = st.session_state.get("lang") or detect_language()
profile = get_profile(lang_code)
t = profile.ui

st.markdown(f"### {t['title']}")
st.caption(t["caption"])

big_default = st.query_params.get("texto_grande", "0") == "1"
big = st.toggle(
    t["big_text"],
    value=st.session_state.get("bigtext", big_default),
    key="bigtext",
)
# Persist in the URL so it survives reloads and can be shared as a link.
if ("1" if big else "0") != st.query_params.get("texto_grande", "0"):
    st.query_params["texto_grande"] = "1" if big else "0"
if big:
    # Scale every rem-based element for low-vision users. Fully ours, no cloud.
    st.markdown("<style>html { font-size: 130%; }</style>", unsafe_allow_html=True)

_, lang_col = st.columns([2, 1], vertical_alignment="bottom")
lang_code = lang_col.selectbox(
    t["lang_label"],
    options=list(PROFILES.keys()),
    index=list(PROFILES.keys()).index(lang_code),
    format_func=lambda c: PROFILES[c].label,
    key="lang",
)
profile = get_profile(lang_code)
t = profile.ui

with st.container(border=True):
    with st.expander(t["photo_section"], expanded=False):
        photo = st.file_uploader(t["photo_upload"], type=["png", "jpg", "jpeg"])
        if photo is not None and st.button(t["photo_button"]):
            with st.spinner(t["photo_working"]):
                try:
                    st.session_state["texto"] = get_ocr().read_text(
                        photo.getvalue(), profile.ocr_lang
                    )
                    st.success(t["photo_ok"])
                except OCRError as e:
                    st.error(str(e))

    texto = st.text_area(
        t["text_label"],
        value=st.session_state.get("texto", ""),
        height=110,
        placeholder=t["text_placeholder"],
    )
    with st.expander(t["advanced"], expanded=False):
        temp = st.slider(t["temp_label"], 0.0, 1.0, 0.2, 0.05)
    run_clicked = st.button(t["explain_button"], type="primary", use_container_width=True)

status_slot = st.empty()
result_slot = st.empty()

scroll_to_result = False

if run_clicked:
    if not texto.strip():
        st.warning(t["need_text"])
    else:
        with status_slot.status(t["working"], expanded=True) as status:
            try:
                res = get_usecase().execute(
                    SimplifyRequest(text=texto, temperature=temp, language=lang_code)
                )
                st.session_state["salida"] = res.output
                st.session_state["salida_lang"] = res.language
                st.session_state["salida_meta"] = (
                    f"{res.model} · {t['cache_hit']}" if res.cached
                    else f"{res.model} · {res.latency_ms}ms · {t['local']}"
                )
                st.session_state.pop("audio", None)
                status.update(label=t["done"], state="complete", expanded=False)
                scroll_to_result = True
            except ValidationError as e:
                st.session_state.pop("salida", None)
                status.update(label=str(e), state="error")
            except LLMError as e:
                st.session_state.pop("salida", None)
                status.update(label=f"{e}. {t['error_server']}", state="error")
            except Exception:
                st.session_state.pop("salida", None)
                status.update(label=t["error_unexpected"], state="error")

# Render from state so the result survives reruns (e.g. pressing Listen).
salida = st.session_state.get("salida")
with result_slot.container():
    if salida:
        st.markdown('<div id="tc-result-anchor"></div>', unsafe_allow_html=True)
        out_profile = get_profile(st.session_state.get("salida_lang", lang_code))
        out_text = out_profile.ui
        with st.container(border=True):
            st.markdown(f"**{out_text['result_title']}**")
            st.markdown(salida)
            meta = st.session_state.get("salida_meta", "")
            st.caption(f"{meta} · {out_profile.label}")
            if st.button(out_text["listen_button"], use_container_width=True):
                with st.spinner(out_text["audio_working"]):
                    try:
                        st.session_state["audio"] = get_tts().synthesize(
                            salida, out_profile.tts_voice
                        )
                    except TTSError as e:
                        st.error(str(e))
            if st.session_state.get("audio"):
                st.audio(st.session_state["audio"], format="audio/wav")
        st.caption(out_text["disclaimer"])

# After a fresh run, bring the answer into view (it may sit below the fold).
# The iframe can execute before the anchor is in the DOM, so retry briefly.
if scroll_to_result:
    try:
        components.html(
            """
            <script>
            (function () {
              var tries = 0;
              var timer = setInterval(function () {
                tries += 1;
                try {
                  var anchor = window.parent.document.getElementById("tc-result-anchor");
                  if (anchor) {
                    anchor.scrollIntoView({ behavior: "smooth", block: "start" });
                    clearInterval(timer);
                  } else if (tries > 25) {
                    clearInterval(timer);
                  }
                } catch (e) { clearInterval(timer); }
              }, 300);
            })();
            </script>
            """,
            height=0,
        )
    except Exception:
        # Scrolling is a convenience: never break the demo if the API changes.
        pass
