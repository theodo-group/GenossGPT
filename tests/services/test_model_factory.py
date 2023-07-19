import unittest

from genoss.model.fake_llm import FakeLLM, FAKE_LLM_NAME
from genoss.model.gpt4all_llm import Gpt4AllLLM
from genoss.services.model_factory import ModelFactory


class TestModelFactory(unittest.TestCase):
    def test_get_model_from_name_gpt(self):
        model = ModelFactory.get_model_from_name('gPt687698')
        self.assertIsInstance(model, Gpt4AllLLM)

    def test_get_model_from_name_fake(self):
        model = ModelFactory.get_model_from_name(FAKE_LLM_NAME)
        self.assertIsInstance(model, FakeLLM)

    def test_get_model_from_name_unknown(self):
        model = ModelFactory.get_model_from_name('unknown')
        self.assertIsNone(model)