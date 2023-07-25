from genoss.llm.hf_hub.base_hf_hub import BaseHuggingFaceHubLLM


class HuggingFaceHubGPT2LLM(BaseHuggingFaceHubLLM):
    """Class for interacting with Hugging Face GPT2 Inference API. Good for testing."""

    name: str = "gpt2"
    description: str = "Hugging Face GPT2 Test Inference API"
    repo_id = "gpt2"
