from typing import List
from abc import abstractmethod, abstractproperty

from pydantic import BaseModel


class LLM(BaseModel):
    name: str
    description: str
    model_path: str

    def generate_answer(self, prompt: str) -> str:
        return "Hello, world!"

    def generate_embedding(self, prompt: str) -> List[float]:
        return [0.0, 0.0, 0.0]
