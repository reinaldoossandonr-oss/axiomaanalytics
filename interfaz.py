import streamlit as st
from openai import OpenAI
import pandas as pd
import os


# 🔹 VERIFICACIÓN TEMPORAL
st.write(os.getenv("OPENAI_API_KEY"))  # solo para debug, luego lo borras

# Estilos CSS para los mensajes
st.markdown(
    """
    <style>
    .user-message {
        background-color: #f56565 !important;
        color: white !important;
    }
    .assistant-message {
        background-color: #ecc94b !important;
        color: black !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# 🔑 API

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.title("Asistente Bursátil")

# 🔹 Cargar Excel desde el repositorio (ruta relativa)
ruta = "cotizaciones.xlsx"  # <-- Cambiado para que busque el archivo dentro del repo
data = pd.read_excel(ruta)

# 🧠 Inicializar historial
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar historial
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f'<div class="user-message">{message["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="assistant-message">{message["content"]}</div>', unsafe_allow_html=True)

# 💬 Input usuario
user_input = st.chat_input("Haz tu pregunta sobre los datos")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.markdown(f'<div class="user-message">{user_input}</div>', unsafe_allow_html=True)

    # 🔹 Preparar prompt
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
    st.session_state.messages.append({"role": "assistant", "content": respuesta})
    st.markdown(f'<div class="assistant-message">{respuesta}</div>', unsafe_allow_html=True)
