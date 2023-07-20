from typing import Optional

from genoss.llm.base_genoss import BaseGenossLLM
from genoss.llm.fake_llm import FAKE_LLM_NAME, FakeLLM
from genoss.llm.hf_hub.falcon import HuggingFaceHubFalconLLM
from genoss.llm.hf_hub.gpt2 import HuggingFaceHubGPT2LLM
from genoss.llm.hf_hub.llama2 import HuggingFaceHubLlama2LLM
from genoss.llm.local.gpt4all import Gpt4AllLLM
from genoss.llm.openai.openai_llm import OpenAILLM

OPENAI_NAME_LIST = ["gpt-4", "gpt-3.5-turbo"]


class ModelFactory:
    @staticmethod
    def get_model_from_name(name: str, api_key) -> Optional[BaseGenossLLM]:
        if name.lower() in OPENAI_NAME_LIST:
            return OpenAILLM(model_name=name, api_key=api_key)
        if name.lower() == "gpt4all":
            return Gpt4AllLLM()
        if name.lower().startswith("hf-llama2"):
            return HuggingFaceHubLlama2LLM(api_key=api_key)
        if name.lower().startswith("hf-gpt2"):
            return HuggingFaceHubGPT2LLM(api_key=api_key)
        if name.lower().startswith("hf-falcon"):
            return HuggingFaceHubFalconLLM(api_key=api_key)
        elif name == FAKE_LLM_NAME:
            return FakeLLM()
        return None
