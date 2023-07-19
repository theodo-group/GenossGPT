from typing import Optional
from genoss.model.base_genoss_llm import BaseGenossLLM
from genoss.model.fake_llm import FakeLLM, FAKE_LLM_NAME
from genoss.model.gpt4all_llm import Gpt4AllLLM


class ModelFactory:
    @staticmethod
    def get_model_from_name(name: str) -> Optional[BaseGenossLLM]:
        if name.lower().startswith("gpt"):
            return Gpt4AllLLM()
        elif name == FAKE_LLM_NAME:
            return FakeLLM()
        return None
