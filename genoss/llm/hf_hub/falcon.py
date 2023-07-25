from genoss.llm.hf_hub.base_hf_hub import BaseHuggingFaceHubLLM


class HuggingFaceHubFalconLLM(BaseHuggingFaceHubLLM):
    """Class for interacting with Hugging Face Falcon Inference API."""

    name: str = "falcon"
    description: str = "Hugging Face Falcon Inference API"
    repo_id = "tiiuae/falcon-40b"
