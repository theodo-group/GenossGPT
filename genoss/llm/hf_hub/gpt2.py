from genoss.llm.hf_hub.base_hf_hub import BaseHuggingFaceHubLLM


class HuggingFaceHubGPT2LLM(BaseHuggingFaceHubLLM):
    name: str = "gpt2"
    description: str = "Hugging Face GPT2 Test Inference API"
    repo_id = "gpt2"

    """
    Class for interacting with Hugging Face GPT2 Inference API. Good for testing.
    """

    def __init__(self, api_key, *args, **kwargs):
        super().__init__(api_key, *args, **kwargs)
