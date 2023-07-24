from pathlib import Path

from pydantic import validator

from genoss.llm.base_genoss import BaseGenossLLM


class BaseLocalLLM(BaseGenossLLM):
    model_path: str

    @validator("model_path")
    def validate_model_path(cls, v: str) -> str:
        if not Path(v).is_file():
            raise ValueError(f"The provided model path does not exist: {v}")
        return v
