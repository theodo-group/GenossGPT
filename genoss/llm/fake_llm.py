from __future__ import annotations

from typing import Dict

from langchain import LLMChain
from langchain.embeddings import FakeEmbeddings
from langchain.llms import FakeListLLM

from genoss.entities.chat.chat_completion import ChatCompletion
from genoss.llm.base_genoss import BaseGenossLLM
from genoss.prompts.prompt_template import prompt_template

FAKE_LLM_NAME = "fake"


class FakeLLM(BaseGenossLLM):
    name: str = FAKE_LLM_NAME
    description: str = "Fake LLM for testing purpose"

    def generate_answer(self, question: str) -> Dict:
        print("Generating Answer")

        llm = FakeListLLM(responses=["Hello from FakeLLM!"])

        llm_chain = LLMChain(llm=llm, prompt=prompt_template)
        response_text = llm_chain(question)

        print("###################")
        print(response_text)

        answer = response_text["text"]
        chat_completion = ChatCompletion(
            model=self.name, answer=answer, question=question
        )

        return chat_completion.to_dict()

    def generate_embedding(self, text: str):
        model = FakeEmbeddings()
        return model.embed_query(text)
