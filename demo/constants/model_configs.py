import openai
from pydantic import BaseModel, SecretStr

from demo.constants.settings import SETTINGS


class ModelConfig(BaseModel):
    display_name: str
    model_name: str
    api_key: SecretStr
    endpoint_url: str

    def configure_open_ai_module(self) -> None:
        openai.api_key = self.api_key.get_secret_value()
        openai.api_base = self.endpoint_url


AVAILABLE_MODELS = [
    ModelConfig(
        display_name="OpenAI-GPT-4",
        model_name="gpt-4",
        api_key=SETTINGS.openai_api_key,
        endpoint_url=openai.api_base,
    ),
    ModelConfig(
        display_name="OpenAI-GPT-4 (through Genoss)",
        model_name="gpt-4",
        api_key=SETTINGS.openai_api_key,
        endpoint_url=SETTINGS.genoss_endpoint_url,
    ),
    ModelConfig(
        display_name="hf-gpt2",
        model_name="hf-hub/hf-gpt2",
        api_key=SETTINGS.huggingfacehub_api_token,
        endpoint_url=SETTINGS.genoss_endpoint_url,
    ),
    ModelConfig(
        display_name="hf-llama2",
        model_name="hf-hub/meta-llama/Llama-2-7b",
        api_key=SETTINGS.huggingfacehub_api_token,
        endpoint_url=SETTINGS.genoss_endpoint_url,
    ),
]
