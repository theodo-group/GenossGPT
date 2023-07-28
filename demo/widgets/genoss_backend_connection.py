import streamlit as st
from requests import RequestException

from demo.constants.model_configs import AVAILABLE_MODELS, ModelConfig
from demo.constants.settings import SETTINGS


def display_message_if_failing_to_access_genoss() -> None:
    try:
        SETTINGS.ping_genoss_backend()
    except RequestException:
        st.error(
            "The demo couldn't access the Genoss backend. Did you start it ? "
            "(see [README.md](https://github.com/OpenGenenerativeAI/GenossGPT/blob/main/README.md))"
        )


def add_custom_hf_endpoint_if_available_or_display_warning() -> None:
    if SETTINGS.custom_hf_endpoint_url is None:
        st.warning(
            "You didn't set a custom Hugging Face endpoint URL in your .env file. "
            "The corresponding model won't be available. "
            "Add it and restart the demo. "
            "Don't forget to check your Hugging Face API token too. "
            "If you don't have any, you may create your own endpoint "
            "[here](https://huggingface.co/inference-endpoints)."
        )
    else:
        AVAILABLE_MODELS.append(
            ModelConfig(
                display_name="hf-custom/llama",
                model_name=f"hf-inference-endpoint/{SETTINGS.custom_hf_endpoint_url}",
                api_key=SETTINGS.huggingfacehub_api_token,
                endpoint_url=SETTINGS.genoss_endpoint_url,
            )
        )
