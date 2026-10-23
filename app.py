"""Streamlit UI - thin layer over SimplifyTextUseCase."""
import streamlit as st
from src.usecase import SimplifyTextUseCase, ValidationError
from src.domain import SimplifyRequest
from src.llm_client import LLMError

@st.cache_resource
def get_usecase() -> SimplifyTextUseCase:
    return SimplifyTextUseCase()

st.set_page_config(page_title="TramiteClaro local - Spark-X2.6-4B", layout="centered")
st.title("TramiteClaro local")
st.caption("HER Hack-Astron #7 · Spark-X2.6-4B 100% local · No sale de tu maquina")

texto = st.text_area("Pega el texto oficial o indicacion de salud:", height=200,
    placeholder="Ej: Requisitos para turno ANSES, indicacion de farmacia, cartel de defensa civil...")
temp = st.slider("Creatividad (temperature)", 0.0, 1.0, 0.2, 0.05)

if st.button("Explicar en simple", type="primary"):
    if not texto.strip():
        st.warning("Pega un texto primero.")
    else:
        with st.spinner("Spark-X2.6-4B explicando en local..."):
            try:
                res = get_usecase().execute(SimplifyRequest(text=texto, temperature=temp))
                st.markdown(res.output)
                if res.cached:
                    st.caption(f"Cache hit · {res.model} · idempotente")
                else:
                    st.caption(f"{res.model} · {res.latency_ms}ms · local")
                st.info("Ayuda explicativa, no reemplaza al profesional. No pegues datos personales.")
            except ValidationError as e:
                st.warning(str(e))
            except LLMError as e:
                st.error(f"{e}. ¿llama-server en :8080?")
            except Exception:
                st.error("Error inesperado. Revisa el server local.")
