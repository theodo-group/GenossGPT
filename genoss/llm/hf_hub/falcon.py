from genoss.llm.hf_hub.base_hf_hub import BaseHuggingFaceHubLLM


class HuggingFaceHubFalconLLM(BaseHuggingFaceHubLLM):
    name: str = "falcon"
    description: str = "Hugging Face Falcon Inference API"
    repo_id = "tiiuae/falcon-40b"

    """
    Class for interacting with Hugging Face Falcon Inference API
    """

    def __init__(self, api_key, *args, **kwargs):
        super().__init__(api_key, *args, **kwargs)
