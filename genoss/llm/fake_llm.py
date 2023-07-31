from __future__ import annotations

from typing import TYPE_CHECKING

from langchain.embeddings import FakeEmbeddings
from langchain.llms import FakeListLLM

from genoss.llm.base_genoss import BaseGenossLLM

if TYPE_CHECKING:
    from genoss.entities.chat.chat_completion import ChatCompletion
    from genoss.entities.chat.message import Message

FAKE_LLM_NAME = "fake"


class FakeLLM(BaseGenossLLM):
    name: str = FAKE_LLM_NAME
    description: str = "Fake LLM for testing purpose"

    def generate_answer(self, messages: list[Message]) -> ChatCompletion:
        llm = FakeListLLM(responses=["Hello from FakeLLM!"])
        return self._chat_completion_from_langchain_llm(llm=llm, messages=messages)

    def generate_embedding(self, text: str) -> list[float]:
        model = FakeEmbeddings(size=128)
        return model.embed_query(text)
