from abc import ABC
from typing import Any, Literal
from unittest import mock

from langchain import LLMChain
from langchain.llms import HuggingFaceEndpoint

from genoss.entities.chat.chat_completion import ChatCompletion
from genoss.llm.base_genoss import BaseGenossLLM
from genoss.prompts.prompt_template import prompt_template


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

    @mock.patch(
        "huggingface_hub.inference_api.INFERENCE_ENDPOINT", "http://0.0.0.0:8080"
    )
    def generate_answer(self, question: str) -> dict[str, Any]:
        """Generate answer from prompt."""
        llm = HuggingFaceEndpoint(
            endpoint_url=self.endpoint_url,
            huggingfacehub_api_token=self.api_key,
            task=self.task,
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
