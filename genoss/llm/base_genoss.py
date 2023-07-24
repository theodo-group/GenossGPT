import re
from abc import abstractmethod
from ast import Not
from typing import Dict, List

from pydantic import BaseModel


class BaseGenossLLM(BaseModel):
    name: str
    description: str

    @abstractmethod
    def generate_answer(self, prompt: str) -> Dict:
        return NotImplementedError

    @abstractmethod
    def generate_embedding(self, text: str) -> List[float]:
        return NotImplementedError
