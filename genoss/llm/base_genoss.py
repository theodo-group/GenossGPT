from abc import abstractmethod
from typing import Any

from pydantic import BaseModel

from genoss.entities.chat.message import Message


class BaseGenossLLM(BaseModel):
    name: str
    description: str

    @abstractmethod
    def generate_answer(self, messages: list[Message]) -> dict[str, Any]:
        pass

    @abstractmethod
    def generate_embedding(self, text: str) -> list[float]:
        pass
