import unittest

from genoss.llm.fake_llm import FakeLLM, FAKE_LLM_NAME
from genoss.llm.local.gpt4all_llm import Gpt4AllLLM
from genoss.llm.openai.openai_llm import OpenAILLM
from genoss.services.model_factory import ModelFactory


class TestModelFactory(unittest.TestCase):
    def test_get_model_from_name_openai(self):
        model = ModelFactory.get_model_from_name('gpt-4')
        self.assertIsInstance(model, OpenAILLM)

    def test_get_model_from_name_gpt4all(self):
        model = ModelFactory.get_model_from_name('Gpt4all')
        self.assertIsInstance(model, Gpt4AllLLM)

    def test_get_model_from_name_fake(self):
        model = ModelFactory.get_model_from_name(FAKE_LLM_NAME)
        self.assertIsInstance(model, FakeLLM)

    def test_get_model_from_name_unknown(self):
        model = ModelFactory.get_model_from_name('unknown')
        self.assertIsNone(model)

