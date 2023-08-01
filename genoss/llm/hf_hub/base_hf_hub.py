from langchain import HuggingFaceHub

from genoss.entities.chat.chat_completion import ChatCompletion
from genoss.entities.chat.message import Message
from genoss.llm.base_genoss import BaseGenossLLM


class BaseHuggingFaceHubLLM(BaseGenossLLM):
    """Class for interacting with Hugging Face Inference APIs."""

    name: str = "HuggingFaceHubLLM"
    description: str = "Hugging Face Hub Inference API"
    api_key: str | None = None
    repo_id: str

    def generate_answer(self, messages: list[Message]) -> ChatCompletion:
        """Generate answer from prompt."""
        llm = HuggingFaceHub(
            repo_id=self.repo_id, huggingfacehub_api_token=self.api_key
        )
        return self._chat_completion_from_langchain_llm(llm=llm, messages=messages)

    def generate_embedding(self, text: str) -> list[float]:
        """Dummy method to satisfy base class requirement."""
        # TODO: why is this necessary? Architecture issue?
        raise NotImplementedError(
            "This method is not used for Hugging Face Inference API."
        )
