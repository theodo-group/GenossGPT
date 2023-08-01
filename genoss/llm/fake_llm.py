from langchain.embeddings import FakeEmbeddings
from langchain.llms import FakeListLLM

from genoss.entities.chat.chat_completion import ChatCompletion
from genoss.entities.chat.message import Message
from genoss.llm.base_genoss import BaseGenossLLM

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
