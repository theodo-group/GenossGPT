from genoss.llm.hf_hub.base_hf_hub import BaseHuggingFaceHubLLM


class HuggingFaceHubLlama2LLM(BaseHuggingFaceHubLLM):
    """Class for interacting with Hugging Face Llama Inference API."""

    name: str = "llama2"
    description: str = "Hugging Face Llama2 Inference API"
    repo_id = "Llama-2-70b-chat-hf"
