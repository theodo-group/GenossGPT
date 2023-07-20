from genoss.llm.hf_hub.base_hf_hub import BaseHuggingFaceHubLLM


class HuggingFaceHubLlama2LLM(BaseHuggingFaceHubLLM):
    name: str = "llama2"
    description: str = "Hugging Face Llama2 Inference API"
    repo_id = "Llama-2-70b-chat-hf"

    """
    Class for interacting with Hugging Face Llama Inference API
    """

    def __init__(self, api_key, *args, **kwargs):
        super().__init__(api_key, *args, **kwargs)
