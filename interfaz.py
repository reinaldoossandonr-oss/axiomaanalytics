import streamlit as st
from openai import OpenAI
import pandas as pd

# Estilos CSS para cambiar solo colores de las burbujas de chat
st.markdown(
    """
    <style>
    /* Mensajes del usuario */
    .user-message {
        background-color: #f56565 !important;  /* rojo suave */
        color: white !important;
    }
    /* Mensajes del asistente */
    .assistant-message {
        background-color: #ecc94b !important;  /* amarillo */
        color: black !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# 🔑 API
client = OpenAI(api_key="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")

st.title("Asistente Bursátil")

# 🔹 Cargar Excel directamente
ruta = r"C:\Users\Reina\Desktop\Provalue\I+D\Terminal\cotizaciones.xlsx"
data = pd.read_excel(ruta)

# 🧠 Inicializar historial
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar historial
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        # Agregar clase CSS para colores
        if message["role"] == "user":
            st.markdown(f'<div class="user-message">{message["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="assistant-message">{message["content"]}</div>', unsafe_allow_html=True)

# 💬 Input usuario
user_input = st.chat_input("Haz tu pregunta sobre los datos")

if user_input:
    # Mostrar mensaje usuario
    with st.chat_message("user"):
        st.markdown(user_input)

    st.session_state.messages.append({"role": "user", "content": user_input})

    # 🔹 Preparar prompt con tus datos
    data_text = data.to_string(index=False)

    prompt = f"""
    Tengo los siguientes datos:
    {data_text}

    Pregunta: {user_input}

    Instrucciones:
    - Calcula rendimiento y volatilidad si aplica
    - Identifica el activo más rentable y el más riesgoso
    - Devuelve una tabla en formato texto separada con |
    """

    # 🤖 Llamada a GPT
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Eres un analista bursátil experto en mercados financieros."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=800
    )

    respuesta = response.choices[0].message.content

    # Mostrar respuesta
    with st.chat_message("assistant"):
        st.markdown(respuesta)

    st.session_state.messages.append({"role": "assistant", "content": respuesta})