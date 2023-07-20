from typing import Dict

from langchain import HuggingFaceHub, LLMChain

from genoss.model.llm.hf_hub.base_hf_hub import BaseHuggingFaceHubLLM
from genoss.model.prompts.prompt_template import prompt_template


class HuggingFaceHubFalconLLM(BaseHuggingFaceHubLLM):
    name: str = "falcon"
    description: str = "Hugging Face Falcon Inference API"
    repo_id = "tiiuae/falcon-40b"

    """
    Class for interacting with Hugging Face Falcon Inference API
    """

    def __init__(self, api_key, *args, **kwargs):
        super().__init__(api_key, *args, **kwargs)

    def generate_answer(self, question: str) -> Dict:
        """
        Generate answer from prompt
        """

        llm = HuggingFaceHub(
            repo_id=self.repo_id, huggingfacehub_api_token=self.HUGGINGFACEHUB_API_TOKEN
        )  # type: ignore
        llm_chain = LLMChain(prompt=prompt_template, llm=llm)

        response = llm_chain(question)
        print(response)
