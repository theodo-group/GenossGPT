from abc import ABC
from typing import Any

from langchain import HuggingFaceHub, LLMChain

from genoss.entities.chat.chat_completion import ChatCompletion
from genoss.entities.chat.message import Message
from genoss.llm.base_genoss import BaseGenossLLM
from genoss.prompts.prompt_template import prompt_template


class BaseHuggingFaceHubLLM(BaseGenossLLM, ABC):
    """Class for interacting with Hugging Face Inference APIs."""

    # Sub classes must define these
    api_key: str | None = None
    repo_id: str

    def generate_answer(self, messages: list[Message]) -> dict[str, Any]:
        """Generate answer from prompt."""
        llm = HuggingFaceHub(
            repo_id=self.repo_id, huggingfacehub_api_token=self.api_key
        )
        llm_chain = LLMChain(prompt=prompt_template, llm=llm)

        question = messages[-1].content
        response_text = llm_chain(question)

        answer = response_text["text"]

        chat_completion = ChatCompletion(
            model=self.name, question=question, answer=answer
        )

        return chat_completion.to_dict()

    def generate_embedding(self, text: str) -> list[float]:
        """Dummy method to satisfy base class requirement."""
        # TODO: why is this necessary? Architecture issue?
        raise NotImplementedError(
            "This method is not used for Hugging Face Inference API."
        )
