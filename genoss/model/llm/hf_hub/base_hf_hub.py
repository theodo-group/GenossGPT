from fastapi import HTTPException

from genoss.model.llm.base_genoss import BaseGenossLLM


class BaseHuggingFaceHubLLM(BaseGenossLLM):
    HUGGINGFACEHUB_API_TOKEN: str

    """
    Class for interacting with Hugging Face Inference APIs
    """

    def __init__(self, api_key, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if api_key is None:
            raise HTTPException(status_code=403, detail="API key missing")

        self.HUGGINGFACEHUB_API_TOKEN = api_key
