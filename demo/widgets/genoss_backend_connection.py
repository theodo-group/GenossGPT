import streamlit as st
from requests import RequestException

from demo.constants.settings import SETTINGS


def display_message_if_failing_to_access_genoss() -> None:
    try:
        SETTINGS.ping_genoss_backend()
    except RequestException:
        st.error(
            "The demo couldn't access the Genoss backend. Did you start it ? (see [README.md](https://github.com/OpenGenenerativeAI/GenossGPT/blob/main/README.md))"
        )
