from dotenv import load_dotenv
import os
import openai
import streamlit as st

# Load environment variables from .env file
load_dotenv()
api_key = None
# Get API keys from environment variables
huggingface_api_key = os.getenv("HUGGINGFACEHUB_API_TOKEN")
openai_api_key = os.getenv("OPENAI_API_KEY")

with st.sidebar:
    model_name = st.selectbox(
        "Chat API Endpoint",
        options=["gpt-4", "hf-gpt2", "hf-llama2"],
        index=0,
    )

genoss_endpoint = "http://localhost:4321"

st.title("🐂🌈 Genoss")
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "How can I help you?"}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    msg = ""

    # Use the user-provided API key if available, otherwise use the API key from the .env file
    api_key = (
        api_key
        if api_key
        else (huggingface_api_key if model_name.startswith("hf") else openai_api_key)
    )
    if api_key == "" or api_key is None:
        st.error("Please provide an API key")
        st.stop()

    openai.api_key = api_key
    openai.api_base = genoss_endpoint

    try:
        response = openai.ChatCompletion.create(
            model=model_name,
            messages=st.session_state.messages,
        )
        msg = response.choices[0].message
    except Exception as e:
        msg = f"Error: {e}"

    st.empty()

    st.session_state.messages.append(msg)
    try:
        st.chat_message("assistant").write(msg["content"])
    except Exception as e:
        st.error(f"Error: {e}, {msg}")
