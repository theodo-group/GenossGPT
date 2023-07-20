from typing import Optional

from genoss.llm.base_genoss_llm import BaseGenossLLM
from genoss.llm.fake_llm import FAKE_LLM_NAME, FakeLLM
from genoss.llm.local.gpt4all_llm import Gpt4AllLLM
from genoss.llm.openai.openai_llm import OpenAILLM

OPENAI_NAME_LIST = ["gpt-4", "gpt-3.5-turbo"]


class ModelFactory:
    @staticmethod
    def get_model_from_name(name: str) -> Optional[BaseGenossLLM]:
        if name.lower() in OPENAI_NAME_LIST:
            return OpenAILLM()
        if name.lower() == "gpt4all":
            return Gpt4AllLLM()
        if name.lower().startswith("falcon"):
            return HuggingFaceHubFalconLLM(api_key=api_key)
        elif name == FAKE_LLM_NAME:
            return FakeLLM()
        return None
