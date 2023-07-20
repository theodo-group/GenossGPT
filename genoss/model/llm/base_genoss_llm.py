from abc import abstractmethod
from typing import Dict, List

from pydantic import BaseModel


class BaseGenossLLM(BaseModel):
    name: str
    description: str
    model_path: str

    @abstractmethod
    def generate_answer(self, prompt: str) -> Dict:
        print("You need to implement the generate_answer method")

        return {id: 1}

    @abstractmethod
    def generate_embedding(self, text: str) -> List[float]:
        print("You need to implement the generate_embedding method")
        return [0.0, 0.0, 0.0]
