from textblob import TextBlob
import pandas as pd
import streamlit as st
from PIL import Image
from googletrans import Translator
from streamlit_lottie import st_lottie
import json
import os


# =========================================================
# CONFIGURACIÓN
# =========================================================

st.set_page_config(
    page_title="Análisis de Sentimiento",
    page_icon="😊",
    layout="centered"
)


# =========================================================
# TÍTULO
# =========================================================

st.title("😊 Análisis de Sentimiento")

image = Image.open("emoticones.jpg")
st.image(image, use_container_width=True)

st.subheader(
    "Por favor escribe en el campo de texto la frase que deseas analizar"
)


# =========================================================
# TRADUCTOR
# =========================================================

translator = Translator()


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.subheader("📊 Polaridad y Subjetividad")

    st.write(
        """
        **Polaridad:** Indica si el sentimiento expresado en el texto
        es positivo, negativo o neutral.

        Su valor oscila entre **-1** (muy negativo) y **1**
        (muy positivo), con **0** representando un sentimiento neutral.

        **Subjetividad:** Mide cuánto del contenido es subjetivo
        (opiniones, emociones, creencias) frente a objetivo (hechos).

        Va de **0 a 1**, donde 0 es completamente objetivo
        y 1 es completamente subjetivo.
        """
    )


# =========================================================
# FUNCIÓN PARA CARGAR ANIMACIONES
# =========================================================

def cargar_animacion(nombre_archivo):

    if os.path.exists(nombre_archivo):

        with open(nombre_archivo, "r", encoding="utf-8") as source:
            return json.load(source)

    return None


# =========================================================
# ANÁLISIS
# =========================================================

with st.expander("🔍 Analizar texto", expanded=True):

    text = st.text_input(
        "Escribe por favor:",
        placeholder="Ejemplo: Me encanta este libro, es increíble..."
    )

    if text:

        try:

            # -------------------------------------------------
            # TRADUCIR ESPAÑOL → INGLÉS
            # -------------------------------------------------

            translation = translator.translate(
                text,
                src="es",
                dest="en"
            )

            trans_text = translation.text


            # -------------------------------------------------
            # ANALIZAR SENTIMIENTO
            # -------------------------------------------------

            blob = TextBlob(trans_text)

            polarity = round(
                blob.sentiment.polarity,
                2
            )

            subjectivity = round(
                blob.sentiment.subjectivity,
                2
            )


            # -------------------------------------------------
            # MOSTRAR VALORES
            # -------------------------------------------------

            st.write(
                "🌡️ **Polaridad:**",
                polarity
            )

            st.write(
                "🧠 **Subjetividad:**",
                subjectivity
            )


            # -------------------------------------------------
            # DETERMINAR ESTADO
            # -------------------------------------------------

            if polarity > 0:

                estado = "Positivo"
                mensaje = "😊 Es un sentimiento Positivo"
                archivo_json = "feliz.json"

            elif polarity < 0:

                estado = "Negativo"
                mensaje = "😔 Es un sentimiento Negativo"
                archivo_json = "triste.json"

            else:

                estado = "Neutral"
                mensaje = "😐 Es un sentimiento Neutral"
                archivo_json = "normal.json"


            # -------------------------------------------------
            # MOSTRAR RESULTADO
            # -------------------------------------------------

            st.markdown("---")

            st.subheader("Resultado")

            if estado == "Positivo":
                st.success(mensaje)

            elif estado == "Negativo":
                st.error(mensaje)

            else:
                st.info(mensaje)


            # -------------------------------------------------
            # ANIMACIÓN LOTTIE
            # -------------------------------------------------

            animation = cargar_animacion(archivo_json)

            if animation:

                st_lottie(
                    animation,
                    width=350,
                    height=350,
                    key=f"animacion_{estado}"
                )

            else:

                st.warning(
                    f"No se encontró el archivo {archivo_json}"
                )


        except Exception as error:

            st.error(
                "Ocurrió un error al analizar el texto."
            )

            st.warning(
                f"Detalles: {error}"
            )
