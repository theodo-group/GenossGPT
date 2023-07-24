from abc import ABC
from typing import Any

from fastapi import HTTPException
from langchain import HuggingFaceHub, LLMChain
from pydantic import Field

from genoss.entities.chat.chat_completion import ChatCompletion
from genoss.llm.base_genoss import BaseGenossLLM
from genoss.prompts.prompt_template import prompt_template


class BaseHuggingFaceHubLLM(BaseGenossLLM, ABC):
    """Class for interacting with Hugging Face Inference APIs."""

    # Sub classes must define these
    huggingfacehub_api_token: str | None = Field(None)
    repo_id: str | None = None

    def __init__(self, api_key: str | None, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)

        if api_key is None:
            # TODO: is this the right way to make it fail?
            raise HTTPException(status_code=403, detail="API key missing")

        self.huggingfacehub_api_token = api_key

    def generate_answer(self, question: str) -> dict[str, Any]:
        """Generate answer from prompt."""
        llm = HuggingFaceHub(
            repo_id=self.repo_id, huggingfacehub_api_token=self.huggingfacehub_api_token
        )
        llm_chain = LLMChain(prompt=prompt_template, llm=llm)

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
