from abc import abstractmethod

from langchain import LLMChain
from pydantic import BaseModel

from genoss.entities.chat.chat_completion import ChatCompletion
from genoss.entities.chat.message import Message
from genoss.prompts.prompt_template import prompt_template


class BaseGenossLLM(BaseModel):
    name: str
    description: str

    @abstractmethod
    def generate_answer(self, messages: list[Message]) -> ChatCompletion:
        pass

    def _chat_completion_from_langchain_llm(
        self, llm: BaseModel, messages: list[Message]
    ) -> ChatCompletion:
        llm_chain = LLMChain(prompt=prompt_template, llm=llm)

        question = messages[-1].content
        response_text = llm_chain(question)

        answer = response_text["text"]

        return ChatCompletion.from_model_question_answer(
            model=self.name, answer=answer, question=question
        )

    @abstractmethod
    def generate_embedding(self, text: str) -> list[float]:
        pass
