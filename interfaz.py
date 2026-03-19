import streamlit as st
from openai import OpenAI
import pandas as pd
import os


# 🔹 VERIFICACIÓN TEMPORAL
#st.write(os.getenv("OPENAI_API_KEY"))  # solo para debug, luego lo borras


# 🔑 API

# Inicializar cliente con la API Key desde Secrets
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Opcional: debug temporal
#st.write(repr(os.getenv("OPENAI_API_KEY")))  # muestra los caracteres invisibles

st.title("Asistente Bursátil")

# 🔹 Cargar Excel desde el repositorio (ruta relativa)
ruta = "cotizaciones.xlsx"  # <-- Cambiado para que busque el archivo dentro del repo
data = pd.read_excel(ruta)

# 🧠 Inicializar historial
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar historial
for message in st.session_state.messages:
    with st.chat_message(
        message["role"],
        avatar="🧑" if message["role"] == "user" else "🤖"
    ):
        st.markdown(message["content"])

# 💬 Input usuario
user_input = st.chat_input("Haz tu pregunta sobre los datos")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    with st.chat_message("user", avatar="🧑"):
        st.markdown(user_input)

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

    with st.chat_message("assistant", avatar="🤖"):
        st.markdown(respuesta)
