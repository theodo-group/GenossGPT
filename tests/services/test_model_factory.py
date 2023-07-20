import unittest

from genoss.llm.fake_llm import FAKE_LLM_NAME, FakeLLM
from genoss.llm.hf_hub.falcon import HuggingFaceHubFalconLLM
from genoss.llm.hf_hub.gpt2 import HuggingFaceHubGPT2LLM
from genoss.llm.hf_hub.llama2 import HuggingFaceHubLlama2LLM
from genoss.llm.local.gpt4all import Gpt4AllLLM
from genoss.llm.openai.openai_llm import OpenAILLM
from genoss.services.model_factory import ModelFactory


class TestModelFactory(unittest.TestCase):
    def test_get_model_from_name_hf_gpt2(self):
        model = ModelFactory.get_model_from_name("hf-gpt2", "api_key")
        self.assertIsInstance(model, HuggingFaceHubGPT2LLM)

    def test_get_model_from_name_hf_falcon(self):
        model = ModelFactory.get_model_from_name("hf-falcon", "api_key")
        self.assertIsInstance(model, HuggingFaceHubFalconLLM)

    def test_get_model_from_name_hf_llama2(self):
        model = ModelFactory.get_model_from_name("hf-llama2", "api_key")
        self.assertIsInstance(model, HuggingFaceHubLlama2LLM)

    def test_get_model_from_name_openai(self):
        model = ModelFactory.get_model_from_name("gpt-4", "api_key")
        self.assertIsInstance(model, OpenAILLM)

    def test_get_model_from_name_gpt4all(self):
        model = ModelFactory.get_model_from_name("Gpt4all")
        self.assertIsInstance(model, Gpt4AllLLM)

    def test_get_model_from_name_fake(self):
        model = ModelFactory.get_model_from_name(FAKE_LLM_NAME)
        self.assertIsInstance(model, FakeLLM)

    def test_get_model_from_name_unknown(self):
        model = ModelFactory.get_model_from_name("unknown", "")
        self.assertIsNone(model)
