from abc import abstractmethod
from typing import Any

from pydantic import BaseModel


class BaseGenossLLM(BaseModel):
    name: str
    description: str

    @abstractmethod
    def generate_answer(self, prompt: str) -> dict[str, Any]:
        pass

    @abstractmethod
    def generate_embedding(self, text: str) -> list[float]:
        pass
