from textblob import TextBlob
import streamlit as st
from PIL import Image
from googletrans import Translator
from streamlit_lottie import st_lottie
import json
import os
import re


# =========================================================
# CONFIGURACIÓN
# =========================================================

st.set_page_config(
    page_title="MORNING",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# ESTILOS
# =========================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;500;600;700;800;900&display=swap');

* {
    font-family: 'Nunito', sans-serif;
    box-sizing: border-box;
}


/* =========================================================
   FONDO NEGRO CON DEGRADADO SUAVE
   ========================================================= */

.stApp {
    background:
        radial-gradient(
            circle at 12% 15%,
            rgba(101, 199, 245, 0.10) 0%,
            rgba(101, 199, 245, 0.04) 20%,
            transparent 42%
        ),
        radial-gradient(
            circle at 88% 78%,
            rgba(255, 228, 91, 0.09) 0%,
            rgba(255, 228, 91, 0.03) 22%,
            transparent 45%
        ),
        linear-gradient(
            135deg,
            #121217 0%,
            #18181d 45%,
            #1d1d23 100%
        );

    color: #ffffff;
    min-height: 100vh;
}

[data-testid="stAppViewContainer"] {
    background: transparent;
}

[data-testid="stHeader"] {
    background: transparent;
}


/* =========================================================
   CONTENEDOR
   ========================================================= */

.main .block-container {
    max-width: 1250px;
    padding: 55px 60px 80px 60px;
}


/* =========================================================
   TÍTULO PRINCIPAL
   ========================================================= */

.small-title {
    color: #65c7f5;
    font-size: 15px;
    font-weight: 800;
    letter-spacing: 4px;
    margin-bottom: 18px;
}

.main-title {
    color: #ffffff;
    font-size: 88px;
    line-height: 0.92;
    font-weight: 900;
    letter-spacing: -4px;
    margin: 0 0 25px 0;
}

.main-title span {
    color: #ffe45b;
}

.hero-description {
    color: #bdbdc5;
    font-size: 18px;
    line-height: 1.7;
    max-width: 520px;
    margin-bottom: 25px;
}

.tag {
    display: inline-block;
    background: #ffe45b;
    color: #18181d;
    padding: 9px 17px;
    border-radius: 30px;
    font-size: 12px;
    font-weight: 900;
    letter-spacing: 1px;
}


/* =========================================================
   IMAGEN
   ========================================================= */

.image-card {
    background: #f8f8f4;
    border-radius: 35px;
    padding: 18px;
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: 0 25px 70px rgba(0,0,0,0.35);
    transform: rotate(1deg);
    overflow: hidden;
}


/* =========================================================
   TARJETA DE ENTRADA
   ========================================================= */

.input-card {
    background: rgba(35,35,41,0.92);
    border: 1px solid #34343c;
    border-radius: 26px;
    padding: 28px;
    margin-top: 35px;
    box-shadow: 0 15px 35px rgba(0,0,0,0.20);
}

.input-title {
    color: #ffffff;
    font-size: 23px;
    font-weight: 900;
    margin-bottom: 16px;
}


/* =========================================================
   INPUT
   ========================================================= */

.stTextInput > div > div > input {

    background: #f8f8f4 !important;

    color: #18181d !important;

    border: 3px solid #65c7f5 !important;

    border-radius: 16px !important;

    min-height: 58px;

    padding: 15px !important;

    font-size: 17px !important;

    font-weight: 700 !important;
}

.stTextInput label {
    color: #c9c9cf !important;
    font-weight: 700 !important;
}


/* =========================================================
   BOTÓN
   ========================================================= */

.stButton {
    margin-top: 15px;
}

.stButton > button {

    width: 100%;

    min-height: 57px;

    border: none !important;

    border-radius: 17px !important;

    background: #ffe45b !important;

    color: #18181d !important;

    font-size: 18px !important;

    font-weight: 900 !important;

    box-shadow: 0 7px 0 #bda62f;

    transition: 0.18s ease;
}

.stButton > button:hover {

    background: #65c7f5 !important;

    color: #18181d !important;

    transform: translateY(3px);

    box-shadow: 0 4px 0 #397c9e;
}


/* =========================================================
   RESULTADO
   ========================================================= */

.result-card {

    background: #f8f8f4;

    color: #18181d;

    border-radius: 28px;

    padding: 30px;

    margin-top: 30px;

    box-shadow: 0 20px 45px rgba(0,0,0,0.25);
}

.result-title {

    color: #18181d;

    font-size: 28px;

    font-weight: 900;

    text-align: center;

    margin-bottom: 20px;
}


/* =========================================================
   ESTADOS
   ========================================================= */

.estado {

    border-radius: 20px;

    padding: 20px;

    text-align: center;

    font-size: 25px;

    font-weight: 900;

    margin-bottom: 20px;
}

.positivo {

    background: #ffe45b;

    color: #18181d;

    border: 3px solid #18181d;
}

.neutral {

    background: #65c7f5;

    color: #18181d;

    border: 3px solid #18181d;
}

.negativo {

    background: #ff8d9b;

    color: #18181d;

    border: 3px solid #18181d;
}


/* =========================================================
   MÉTRICAS
   ========================================================= */

.metricas {

    display: grid;

    grid-template-columns: 1fr 1fr;

    gap: 15px;

    margin-top: 20px;
}

.metrica {

    background: #e8e8e2;

    border-radius: 18px;

    padding: 20px;

    text-align: center;

    color: #18181d;

    border: 2px solid #d5d5cf;
}

.metrica-nombre {

    font-size: 13px;

    font-weight: 800;

    color: #6d6d74;

    margin-bottom: 7px;
}

.metrica-valor {

    font-size: 31px;

    font-weight: 900;

    color: #18181d;
}


/* =========================================================
   SIDEBAR
   ========================================================= */

section[data-testid="stSidebar"] {

    background:
        linear-gradient(
            180deg,
            #1c1c22 0%,
            #15151a 100%
        );

    border-right: 1px solid #34343c;
}

section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {

    color: #ffe45b !important;

    font-weight: 900 !important;
}

section[data-testid="stSidebar"] p {

    color: #d0d0d5 !important;

    line-height: 1.7;

    font-size: 15px;
}

.sidebar-title {
    color: #65c7f5;
    font-size: 23px;
    font-weight: 900;
    margin-bottom: 20px;
}

.sidebar-section-title {
    color: #ffe45b;
    font-size: 18px;
    font-weight: 900;
    margin-top: 20px;
    margin-bottom: 8px;
}


/* =========================================================
   ANIMACIÓN
   ========================================================= */

.lottie-box {

    background: #ffffff;

    border-radius: 25px;

    padding: 15px;

    margin-top: 25px;

    display: flex;

    justify-content: center;
}


/* =========================================================
   SCROLLBAR
   ========================================================= */

html {
    scrollbar-width: thin;
    scrollbar-color: #ffe45b #18181d;
}

::-webkit-scrollbar {
    width: 10px;
}

::-webkit-scrollbar-track {
    background: #18181d;
}

::-webkit-scrollbar-thumb {
    background: #ffe45b;
    border-radius: 20px;
}


/* =========================================================
   OCULTAR ELEMENTOS
   ========================================================= */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# TRADUCTOR
# =========================================================

translator = Translator()


# =========================================================
# FUNCIÓN PARA CARGAR ANIMACIONES
# =========================================================

def cargar_animacion(nombre):

    if not os.path.exists(nombre):
        return None

    try:

        with open(
            nombre,
            "r",
            encoding="utf-8"
        ) as archivo:

            return json.load(archivo)

    except Exception:

        return None


# =========================================================
# PALABRAS POSITIVAS
# =========================================================

palabras_positivas = {
    "feliz",
    "felices",
    "felicidad",
    "amor",
    "amar",
    "amo",
    "amado",
    "amada",
    "excelente",
    "excelentes",
    "genial",
    "geniales",
    "increible",
    "increíble",
    "increibles",
    "increíbles",
    "maravilloso",
    "maravillosa",
    "maravillosos",
    "maravillosas",
    "bueno",
    "buena",
    "buen",
    "buenos",
    "buenas",
    "bien",
    "fantastico",
    "fantástico",
    "fantastica",
    "fantástica",
    "perfecto",
    "perfecta",
    "perfectos",
    "perfectas",
    "mejor",
    "mejores",
    "agradable",
    "agradables",
    "divertido",
    "divertida",
    "divertidos",
    "divertidas",
    "sonrisa",
    "sonreir",
    "sonreír",
    "gracias",
    "agradecido",
    "agradecida",
    "gustar",
    "gusta",
    "encanta",
    "encantado",
    "encantada",
    "victoria",
    "exito",
    "éxito",
    "ganar",
    "gané",
    "ganado",
    "hermoso",
    "hermosa",
    "lindo",
    "linda"
}


# =========================================================
# PALABRAS NEGATIVAS
# =========================================================

palabras_negativas = {
    "triste",
    "tristes",
    "tristeza",
    "odio",
    "odiar",
    "odioso",
    "odiosa",
    "malo",
    "mala",
    "malos",
    "malas",
    "mal",
    "terrible",
    "terribles",
    "horrible",
    "horribles",
    "horrendo",
    "horrenda",
    "dolor",
    "doloroso",
    "dolorosa",
    "enojado",
    "enojada",
    "enojo",
    "rabia",
    "furia",
    "molesto",
    "molesta",
    "molestia",
    "problema",
    "problemas",
    "fracaso",
    "fracasar",
    "perder",
    "perdí",
    "perdido",
    "miedo",
    "temor",
    "preocupado",
    "preocupada",
    "preocupación",
    "llorar",
    "lloro",
    "llanto",
    "feo",
    "fea",
    "feos",
    "feas",
    "decepcionado",
    "decepcionada",
    "decepción",
    "mentira",
    "mentiroso",
    "mentirosa",
    "culpa",
    "culpable",
    "injusto",
    "injusta",
    "difícil",
    "dificil",
    "aburrido",
    "aburrida",
    "aburrimiento",
    "cansado",
    "cansada",
    "cansancio"
}


# =========================================================
# ANALIZAR PALABRAS EN ESPAÑOL
# =========================================================

def analizar_espanol(texto):

    palabras = re.findall(
        r"[a-záéíóúüñ]+",
        texto.lower()
    )

    positivas = 0
    negativas = 0

    for palabra in palabras:

        if palabra in palabras_positivas:
            positivas += 1

        if palabra in palabras_negativas:
            negativas += 1

    return positivas, negativas


# =========================================================
# HERO
# =========================================================

col_izquierda, col_derecha = st.columns(
    [1.05, 0.95],
    gap="large"
)


# =========================================================
# PARTE IZQUIERDA
# =========================================================

with col_izquierda:

    st.markdown(
        '<div class="small-title">SENTIMENT ANALYSIS</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="main-title">
            MORNING<br>
            <span>FEELINGS.</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="hero-description">
            Escribe cualquier frase y descubre si expresa
            un sentimiento positivo, neutral o negativo.
            MORNING analiza tus palabras y transforma
            el resultado en una expresión visual.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="tag">😊 DISCOVER YOUR MOOD</div>',
        unsafe_allow_html=True
    )


# =========================================================
# PARTE DERECHA
# =========================================================

with col_derecha:

    st.markdown(
        '<div class="image-card">',
        unsafe_allow_html=True
    )

    image = Image.open(
        "emoticones.jpg"
    )

    st.image(
        image,
        use_container_width=True
    )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


# =========================================================
# CAMPO DE TEXTO
# =========================================================

st.markdown(
    """
    <div class="input-card">

        <div class="input-title">
            💬 ¿Cómo te sientes hoy?
        </div>
    """,
    unsafe_allow_html=True
)

texto = st.text_input(
    "Escribe tu frase",
    placeholder="Ejemplo: Hoy estoy muy feliz porque todo salió increíble.",
    label_visibility="collapsed"
)

enviar = st.button(
    "☀️ ANALIZAR SENTIMIENTO"
)

st.markdown(
    "</div>",
    unsafe_allow_html=True
)


# =========================================================
# SIDEBAR - INDICACIONES
# =========================================================

with st.sidebar:

    st.markdown(
        '<div class="sidebar-title">Polaridad y Subjetividad</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="sidebar-section-title">
            Polaridad
        </div>

        <p>
        Indica si el sentimiento expresado en el texto
        es positivo, negativo o neutral.
        Su valor oscila entre <b>-1</b> (muy negativo)
        y <b>1</b> (muy positivo), con <b>0</b>
        representando un sentimiento neutral.
        </p>

        <div class="sidebar-section-title">
            Subjetividad
        </div>

        <p>
        Mide cuánto del contenido es subjetivo
        (opiniones, emociones, creencias) frente a
        objetivo (hechos).
        Va de <b>0</b> a <b>1</b>, donde <b>0</b>
        es completamente objetivo y <b>1</b>
        es completamente subjetivo.
        </p>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# ANALIZAR AL PRESIONAR EL BOTÓN
# =========================================================

if enviar:

    if not texto.strip():

        st.warning(
            "Escribe una frase antes de analizar."
        )

    else:

        try:

            # -------------------------------------------------
            # PALABRAS EN ESPAÑOL
            # -------------------------------------------------

            positivas_es, negativas_es = analizar_espanol(
                texto
            )


            # -------------------------------------------------
            # TRADUCCIÓN
            # -------------------------------------------------

            with st.spinner(
                "Analizando..."
            ):

                traduccion = translator.translate(
                    texto,
                    src="es",
                    dest="en"
                )

                texto_ingles = traduccion.text


                # -------------------------------------------------
                # TEXTBLOB
                # -------------------------------------------------

                blob = TextBlob(
                    texto_ingles
                )

                polaridad_blob = (
                    blob.sentiment.polarity
                )

                subjetividad = (
                    blob.sentiment.subjectivity
                )


            # -------------------------------------------------
            # DETERMINAR SENTIMIENTO
            # -------------------------------------------------

            if positivas_es > negativas_es:

                polaridad = max(
                    0.1,
                    round(polaridad_blob, 2)
                )

                sentimiento = "POSITIVO"

                emoji = "😊"

                archivo_json = "feliz.json"

                clase = "positivo"


            elif negativas_es > positivas_es:

                polaridad = min(
                    -0.1,
                    round(polaridad_blob, 2)
                )

                sentimiento = "NEGATIVO"

                emoji = "😔"

                archivo_json = "triste.json"

                clase = "negativo"


            else:

                polaridad = round(
                    polaridad_blob,
                    2
                )

                if polaridad > 0:

                    sentimiento = "POSITIVO"

                    emoji = "😊"

                    archivo_json = "feliz.json"

                    clase = "positivo"

                elif polaridad < 0:

                    sentimiento = "NEGATIVO"

                    emoji = "😔"

                    archivo_json = "triste.json"

                    clase = "negativo"

                else:

                    sentimiento = "NEUTRAL"

                    emoji = "😐"

                    archivo_json = "normal.json"

                    clase = "neutral"


            # =================================================
            # TARJETA DE RESULTADO
            # =================================================

            st.markdown(
                '<div class="result-card">',
                unsafe_allow_html=True
            )

            st.markdown(
                '<div class="result-title">RESULTADO</div>',
                unsafe_allow_html=True
            )


            # =================================================
            # ESTADO
            # =================================================

            st.markdown(
                f"""
                <div class="estado {clase}">
                    {emoji}<br>
                    {sentimiento}
                </div>
                """,
                unsafe_allow_html=True
            )


            # =================================================
            # MÉTRICAS - CORREGIDAS
            # =================================================

            st.markdown(
                f"""
                <div class="metricas">

                    <div class="metrica">

                        <div class="metrica-nombre">
                            POLARIDAD
                        </div>

                        <div class="metrica-valor">
                            {polaridad}
                        </div>

                    </div>

                    <div class="metrica">

                        <div class="metrica-nombre">
                            SUBJETIVIDAD
                        </div>

                        <div class="metrica-valor">
                            {round(subjetividad, 2)}
                        </div>

                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )


            # =================================================
            # FRASE ANALIZADA
            # =================================================

            st.markdown(
                f"""
                <div style="
                    margin-top:20px;
                    padding:18px;
                    background:#eeeeea;
                    border-radius:17px;
                    color:#18181d;
                    font-weight:700;
                    line-height:1.6;
                ">
                    <b>Frase analizada:</b><br>
                    "{texto}"
                </div>
                """,
                unsafe_allow_html=True
            )


            st.markdown(
                "</div>",
                unsafe_allow_html=True
            )


            # =================================================
            # ANIMACIÓN
            # =================================================

            animation = cargar_animacion(
                archivo_json
            )

            if animation:

                st.markdown(
                    f"""
                    <div style="
                        text-align:center;
                        color:#ffffff;
                        font-size:19px;
                        font-weight:900;
                        margin-top:35px;
                    ">
                        {emoji} ESTADO DETECTADO
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st_lottie(
                    animation,
                    width=350,
                    height=350,
                    key=f"animation_{sentimiento}"
                )

            else:

                st.error(
                    f"No se encontró {archivo_json}"
                )


        except Exception as error:

            st.error(
                "No se pudo analizar la frase."
            )

            st.warning(
                f"Detalles: {error}"
            )
