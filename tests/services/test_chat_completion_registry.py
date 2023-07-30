import pytest

from genoss.llm.base_genoss import BaseGenossLLM
from genoss.llm.fake_llm import FAKE_LLM_NAME, FakeLLM
from genoss.llm.hf_hub.base_hf_hub import BaseHuggingFaceHubLLM
from genoss.llm.local.gpt4all import Gpt4AllLLM
from genoss.llm.openai.openai_llm import OpenAILLM
from genoss.services.chat_completion_registry import chat_completion_registry


class TestChatCompletionRegistry:
    @staticmethod
    @pytest.mark.parametrize(
        ("model_name", "model_class"),
        [
            ("hf-hub/gpt2", BaseHuggingFaceHubLLM),
            ("hf-hub/tiiuae/falcon-40b", BaseHuggingFaceHubLLM),
            ("hf-hub/Llama-2-70b-chat-hf", BaseHuggingFaceHubLLM),
            ("gpt-4", OpenAILLM),
            ("openai/gpt-4", OpenAILLM),
            ("gpt4all", Gpt4AllLLM),
            (FAKE_LLM_NAME, FakeLLM),
        ],
    )
    def test_get_model_from_name(model_name: str, model_class: type[BaseGenossLLM]):
        model = chat_completion_registry.build_model(
            path=model_name, call_params={"api_key": "api_key"}
        )
        assert isinstance(model, model_class)

    @staticmethod
    def test_get_model_from_name_unknown():
        # TODO: we do not force model_name anymore.
        # Should we check it ? There could be a new model_name that does not exist yet.
        # Do we want to block it ?
        # TODO: Commenting for the time being
        # model = chat_completion_registry.build_model(
        #     path="unknown", call_params={"api_key": ""}
        # )
        # assert model is None
        pass
