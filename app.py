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
    page_title="SmileTime - Análisis de Sentimiento",
    page_icon="😊",
    layout="centered"
)


# =========================================================
# INTERFAZ - ESTILO SMILETIME
# =========================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&display=swap');

* {
    font-family: 'Nunito', sans-serif;
}

/* =========================================================
   FONDO
   ========================================================= */

.stApp {
    background: #f27dde;
    color: #111111;
}

[data-testid="stAppViewContainer"] {
    background: #f27dde;
}

[data-testid="stHeader"] {
    background: transparent;
}


/* =========================================================
   CONTENEDOR
   ========================================================= */

.main .block-container {
    max-width: 850px;
    padding-top: 35px;
    padding-bottom: 60px;
}


/* =========================================================
   TÍTULO
   ========================================================= */

h1 {
    color: #111111 !important;
    font-size: 46px !important;
    font-weight: 900 !important;
    text-align: center;
    letter-spacing: -1px;
    margin-bottom: 5px !important;
}

.subtitulo {
    text-align: center;
    color: #111111;
    font-size: 18px;
    font-weight: 700;
    margin-bottom: 25px;
}


/* =========================================================
   LOGO
   ========================================================= */

.logo-smile {
    width: 95px;
    height: 95px;
    background: #ffe500;
    border: 5px solid #111111;
    border-radius: 50%;
    margin: 0 auto 15px auto;

    display: flex;
    align-items: center;
    justify-content: center;

    font-size: 55px;

    box-shadow:
        6px 7px 0px #111111;
}


/* =========================================================
   TARJETAS
   ========================================================= */

.card {
    background: #fffbea;
    border: 4px solid #111111;
    border-radius: 28px;

    padding: 25px;

    box-shadow:
        7px 8px 0px #111111;

    margin-bottom: 25px;
}

.card-title {
    color: #111111;
    font-size: 24px;
    font-weight: 900;
    margin-bottom: 15px;
}


/* =========================================================
   CAMPO DE TEXTO
   ========================================================= */

.stTextInput > div > div > input {
    background: #ffffff !important;

    color: #111111 !important;

    border: 4px solid #111111 !important;

    border-radius: 16px !important;

    font-size: 17px !important;

    font-weight: 700 !important;

    padding: 15px !important;

    box-shadow:
        4px 5px 0px #111111;
}

.stTextInput label {
    color: #111111 !important;
    font-weight: 900 !important;
    font-size: 17px !important;
}


/* =========================================================
   BOTÓN ENVIAR
   ========================================================= */

.stButton {
    display: flex;
    justify-content: center;
}

.stButton > button {

    width: 100%;

    min-height: 60px;

    background: #32d95b !important;

    color: #111111 !important;

    border: 4px solid #111111 !important;

    border-radius: 18px !important;

    font-size: 21px !important;

    font-weight: 900 !important;

    box-shadow:
        6px 7px 0px #111111;

    transition: 0.15s ease;
}

.stButton > button:hover {

    background: #ffe500 !important;

    color: #111111 !important;

    transform: translate(
        2px,
        2px
    );

    box-shadow:
        3px 4px 0px #111111;
}


/* =========================================================
   RESULTADO
   ========================================================= */

.resultado {

    background: #ffffff;

    border: 4px solid #111111;

    border-radius: 25px;

    padding: 25px;

    box-shadow:
        7px 8px 0px #111111;

    margin-top: 25px;
}

.resultado-titulo {

    color: #111111;

    font-size: 27px;

    font-weight: 900;

    text-align: center;

    margin-bottom: 15px;
}


/* =========================================================
   VALORES
   ========================================================= */

.valor {

    background: #ffe500;

    border: 3px solid #111111;

    border-radius: 15px;

    padding: 13px;

    margin: 8px 0;

    color: #111111;

    font-size: 17px;

    font-weight: 900;

    text-align: center;
}


/* =========================================================
   ESTADOS
   ========================================================= */

.estado-positivo {

    background: #32d95b;

    border: 4px solid #111111;

    border-radius: 20px;

    padding: 18px;

    color: #111111;

    font-size: 25px;

    font-weight: 900;

    text-align: center;

    margin: 20px 0;
}

.estado-neutral {

    background: #ffffff;

    border: 4px solid #111111;

    border-radius: 20px;

    padding: 18px;

    color: #111111;

    font-size: 25px;

    font-weight: 900;

    text-align: center;

    margin: 20px 0;
}

.estado-negativo {

    background: #ff4fa3;

    border: 4px solid #111111;

    border-radius: 20px;

    padding: 18px;

    color: #111111;

    font-size: 25px;

    font-weight: 900;

    text-align: center;

    margin: 20px 0;
}


/* =========================================================
   SIDEBAR
   ========================================================= */

section[data-testid="stSidebar"] {

    background: #ffe500;

    border-right: 4px solid #111111;
}

section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {

    color: #111111 !important;

    font-weight: 900 !important;
}

section[data-testid="stSidebar"] p {

    color: #111111 !important;

    font-weight: 700;

    line-height: 1.6;
}


/* =========================================================
   EXPANDER
   ========================================================= */

.streamlit-expanderHeader {

    background: #ffffff !important;

    color: #111111 !important;

    border: 3px solid #111111 !important;

    border-radius: 15px !important;

    font-weight: 900 !important;
}


/* =========================================================
   ALERTAS
   ========================================================= */

div[data-testid="stAlert"] {

    border: 3px solid #111111;

    border-radius: 15px;

    color: #111111;
}


/* =========================================================
   LOTTIE
   ========================================================= */

.lottie-container {

    display: flex;

    justify-content: center;
}


/* =========================================================
   BARRA DE DESPLAZAMIENTO
   ========================================================= */

html {

    scrollbar-width: thin;

    scrollbar-color:
        #111111
        #f27dde;
}

::-webkit-scrollbar {

    width: 12px;
}

::-webkit-scrollbar-track {

    background: #f27dde;
}

::-webkit-scrollbar-thumb {

    background: #111111;

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
# LOGO
# =========================================================

st.markdown(
    '<div class="logo-smile">😊</div>',
    unsafe_allow_html=True
)


# =========================================================
# TÍTULO
# =========================================================

st.title("SMILETIME")

st.markdown(
    '<div class="subtitulo">¿Qué sentimiento tiene tu frase?</div>',
    unsafe_allow_html=True
)


# =========================================================
# IMAGEN
# =========================================================

image = Image.open("emoticones.jpg")

st.image(
    image,
    use_container_width=True
)


# =========================================================
# TRADUCTOR
# =========================================================

translator = Translator()


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.subheader("😊 Análisis de sentimiento")

    st.write(
        """
        **POLARIDAD**

        Indica si el sentimiento es:

        🟢 Positivo  
        ⚪ Neutral  
        🩷 Negativo  

        La polaridad va desde:

        **-1 → 1**

        **SUBJETIVIDAD**

        Mide cuánto expresa:

        💭 Opiniones  
        ❤️ Emociones  
        🗣️ Creencias  

        Va desde:

        **0 → 1**
        """
    )

    st.markdown("---")

    st.write(
        "Escribe una frase y presiona **ENVIAR**."
    )


# =========================================================
# FUNCIÓN PARA CARGAR LOTTIE
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
# PALABRAS POSITIVAS EN ESPAÑOL
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
    "linda",
    "genial"
}


# =========================================================
# PALABRAS NEGATIVAS EN ESPAÑOL
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
    "decepcion",
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

    texto_limpio = texto.lower()

    palabras = re.findall(
        r"[a-záéíóúüñ]+",
        texto_limpio
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
# CAMPO DE TEXTO
# =========================================================

st.markdown(
    """
    <div class="card">
        <div class="card-title">
            💬 Escribe tu frase
        </div>
    """,
    unsafe_allow_html=True
)

texto = st.text_input(
    "Tu mensaje",
    placeholder="Ejemplo: Me encanta este día, estoy muy feliz 😊",
    label_visibility="collapsed"
)

enviar = st.button(
    "🚀 ENVIAR",
    use_container_width=True
)

st.markdown(
    "</div>",
    unsafe_allow_html=True
)


# =========================================================
# ANALIZAR CUANDO SE PRESIONA ENVIAR
# =========================================================

if enviar:

    if not texto.strip():

        st.warning(
            "✏️ Primero escribe una frase."
        )

    else:

        try:

            # =================================================
            # ANALIZAR PALABRAS EN ESPAÑOL
            # =================================================

            positivas_es, negativas_es = analizar_espanol(
                texto
            )


            # =================================================
            # TRADUCIR A INGLÉS
            # =================================================

            with st.spinner(
                "😊 Analizando tu frase..."
            ):

                traduccion = translator.translate(
                    texto,
                    src="es",
                    dest="en"
                )

                texto_ingles = traduccion.text


                # =================================================
                # TEXTBLOB
                # =================================================

                blob = TextBlob(
                    texto_ingles
                )

                polaridad_textblob = (
                    blob.sentiment.polarity
                )

                subjetividad = (
                    blob.sentiment.subjectivity
                )


            # =================================================
            # DECISIÓN DE SENTIMIENTO
            # =================================================
            #
            # Si las palabras españolas detectan claramente
            # un sentimiento, se utilizan para reforzarlo.
            # Si no, se utiliza TextBlob.
            # =================================================

            if positivas_es > negativas_es:

                polaridad = max(
                    0.1,
                    round(polaridad_textblob, 2)
                )

                sentimiento = "POSITIVO"

                emoji = "😊"

                archivo_json = "feliz.json"

            elif negativas_es > positivas_es:

                polaridad = min(
                    -0.1,
                    round(polaridad_textblob, 2)
                )

                sentimiento = "NEGATIVO"

                emoji = "😔"

                archivo_json = "triste.json"

            else:

                polaridad = round(
                    polaridad_textblob,
                    2
                )

                if polaridad > 0:

                    sentimiento = "POSITIVO"

                    emoji = "😊"

                    archivo_json = "feliz.json"

                elif polaridad < 0:

                    sentimiento = "NEGATIVO"

                    emoji = "😔"

                    archivo_json = "triste.json"

                else:

                    sentimiento = "NEUTRAL"

                    emoji = "😐"

                    archivo_json = "normal.json"


            # =================================================
            # MOSTRAR RESULTADO
            # =================================================

            st.markdown(
                '<div class="resultado">',
                unsafe_allow_html=True
            )

            st.markdown(
                '<div class="resultado-titulo">'
                'RESULTADO'
                '</div>',
                unsafe_allow_html=True
            )


            # =================================================
            # ESTADO
            # =================================================

            if sentimiento == "POSITIVO":

                st.markdown(
                    f"""
                    <div class="estado-positivo">
                        {emoji}<br>
                        ¡SENTIMIENTO POSITIVO!
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            elif sentimiento == "NEGATIVO":

                st.markdown(
                    f"""
                    <div class="estado-negativo">
                        {emoji}<br>
                        SENTIMIENTO NEGATIVO
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            else:

                st.markdown(
                    f"""
                    <div class="estado-neutral">
                        {emoji}<br>
                        SENTIMIENTO NEUTRAL
                    </div>
                    """,
                    unsafe_allow_html=True
                )


            # =================================================
            # VALORES
            # =================================================

            st.markdown(
                f"""
                <div class="valor">
                    📈 Polaridad: {polaridad}
                </div>

                <div class="valor">
                    🧠 Subjetividad: {round(subjetividad, 2)}
                </div>
                """,
                unsafe_allow_html=True
            )


            st.markdown(
                f"""
                <p style="
                    text-align:center;
                    font-weight:800;
                    color:#111111;
                    font-size:17px;
                ">
                    "{texto}"
                </p>
                """,
                unsafe_allow_html=True
            )


            st.markdown(
                "</div>",
                unsafe_allow_html=True
            )


            # =================================================
            # LOTTIE
            # =================================================

            animation = cargar_animacion(
                archivo_json
            )

            if animation:

                st.markdown(
                    f"""
                    <div style="
                        text-align:center;
                        color:#111111;
                        font-weight:900;
                        font-size:18px;
                        margin-top:25px;
                    ">
                        {emoji} Estado detectado
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st_lottie(
                    animation,
                    width=350,
                    height=350,
                    key=f"lottie_{archivo_json}"
                )

            else:

                st.error(
                    f"No se encontró {archivo_json}"
                )


        except Exception as error:

            st.error(
                "❌ No se pudo analizar la frase."
            )

            st.warning(
                f"Detalles: {error}"
            )
