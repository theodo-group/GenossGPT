from abc import ABC
from typing import Literal

from langchain.llms import HuggingFaceEndpoint

from genoss.entities.chat.chat_completion import ChatCompletion
from genoss.entities.chat.message import Message
from genoss.llm.base_genoss import BaseGenossLLM


class HuggingFaceInferenceEndpointLLM(BaseGenossLLM, ABC):
    """Class for interacting with Hugging Face Inference APIs."""

    # Subclasses must define these
    name = "HF Inference Endpoint"
    api_key: str | None = None
    endpoint_url: str
    description: str = "Hugging Face Inference API custom endpoint."
    task: Literal[
        "text-generation", "text-generation", "summarization"
    ] = "text-generation"

    def generate_answer(self, messages: list[Message]) -> ChatCompletion:
        """Generate answer from prompt."""
        llm = HuggingFaceEndpoint(
            endpoint_url=self.endpoint_url,
            huggingfacehub_api_token=self.api_key,
            task=self.task,
        )
        return self._chat_completion_from_langchain_llm(llm=llm, messages=messages)

    def generate_embedding(self, text: str) -> list[float]:
        """Dummy method to satisfy base class requirement."""
        # TODO: why is this necessary? Architecture issue?
        raise NotImplementedError(
            "This method is not used for Hugging Face Inference API."
        )
