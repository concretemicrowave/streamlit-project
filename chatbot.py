import os
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY")
MODEL = "llama-3.1-8b-instant"


@st.cache_resource
def get_client():
    return Groq(api_key=API_KEY)

def render():
    if "bot_messages" not in st.session_state:
        st.session_state.bot_messages = []

    for m in st.session_state.bot_messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

    question = st.chat_input("Ask the bot", key="bot_input")
    if not question:
        return

    st.session_state.bot_messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        stream = get_client().chat.completions.create(
            model=MODEL,
            messages=st.session_state.bot_messages,
            stream=True,
        )
        answer = st.write_stream(chunk.choices[0].delta.content or "" for chunk in stream)

    st.session_state.bot_messages.append({"role": "assistant", "content": answer})
