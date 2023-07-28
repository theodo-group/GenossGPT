"""Streamlit app for Genoss demo.

Start from project root with :
```bash
PYTHONPATH=. streamlit run demo/main.py
```
Don't forget to set .env variables before running the app.
"""

import openai
import streamlit as st

from demo.constants.model_configs import AVAILABLE_MODELS, ModelConfig
from demo.constants.paths import ROOT_FOLDER
from demo.widgets.genoss_backend_connection import (
    add_custom_hf_endpoint_if_available_or_display_warning,
    display_message_if_failing_to_access_genoss,
)

st.set_page_config(
    "Genoss Demo",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon=str(ROOT_FOLDER / "doc/assets/logo.png"),
)

with st.sidebar:
    display_message_if_failing_to_access_genoss()
    add_custom_hf_endpoint_if_available_or_display_warning()

    selected_model: ModelConfig = st.selectbox(
        "Chat API Endpoint",
        options=AVAILABLE_MODELS,
        index=0,
        format_func=lambda model: model.display_name,
    )
    selected_model.configure_open_ai_module()

st.title("🐂🌈 Genoss")
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {
            "role": "system",
            "content": "You are a friendly chatbot made by the builders of Quivr.app. Answer all questions to the best of your ability. If you don't know the answer, just say that you don't know, don't try to make up an answer",
        },
        {"role": "assistant", "content": "How can I help you?"},
    ]

for msg in st.session_state.messages:
    if msg["role"] == "system":
        st.markdown(f"System Prompt: *{msg['content']}*")
        continue
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    msg = ""

    try:
        response = openai.ChatCompletion.create(
            model=selected_model.model_name,
            messages=st.session_state.messages,
        )
        msg = response.choices[0].message
    except Exception as e:
        st.error(e)
        st.stop()

    st.empty()

    st.session_state.messages.append(msg)
    st.chat_message("assistant").write(msg["content"])
