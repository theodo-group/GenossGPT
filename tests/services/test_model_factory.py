import pytest

from genoss.llm.base_genoss import BaseGenossLLM
from genoss.llm.fake_llm import FAKE_LLM_NAME, FakeLLM
from genoss.llm.hf_hub.falcon import HuggingFaceHubFalconLLM
from genoss.llm.hf_hub.gpt2 import HuggingFaceHubGPT2LLM
from genoss.llm.hf_hub.llama2 import HuggingFaceHubLlama2LLM
from genoss.llm.local.gpt4all import Gpt4AllLLM
from genoss.llm.openai_llm.openai_llm import OpenAILLM
from genoss.services.model_factory import ModelFactory


class TestModelFactory:
    @staticmethod
    @pytest.mark.parametrize(
        ("model_name", "model_class"),
        [
            ("hf-gpt2", HuggingFaceHubGPT2LLM),
            ("hf-falcon", HuggingFaceHubFalconLLM),
            ("hf-llama2", HuggingFaceHubLlama2LLM),
            ("gpt-4", OpenAILLM),
            ("Gpt4all", Gpt4AllLLM),
            (FAKE_LLM_NAME, FakeLLM),
        ],
    )
    def test_get_model_from_name(model_name: str, model_class: type[BaseGenossLLM]):
        model = ModelFactory.get_model_from_name(name=model_name, api_key="api_key")
        assert isinstance(model, model_class)

    @staticmethod
    def test_get_model_from_name_unknown():
        model = ModelFactory.get_model_from_name("unknown", "")
        assert model is None
