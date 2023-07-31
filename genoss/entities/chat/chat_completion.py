import time
import uuid
from typing import Self

from pydantic import BaseModel, Field

from genoss.entities.chat.message import Message


class Choice(BaseModel):
    message: Message
    finish_reason: str = "stop"
    index: int = 0

    @classmethod
    def from_model_answer(cls, answer: str) -> Self:
        return cls(
            message=Message(role="assistant", content=answer),
            finish_reason="stop",
            index=0,
        )


class Usage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int

    @classmethod
    def from_question_and_answer(cls, question: str, answer: str) -> Self:
        return cls(
            prompt_tokens=len(question),
            completion_tokens=len(answer),
            total_tokens=len(question) + len(answer),
        )


class ChatCompletion(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    object: str = "chat.completion"
    created: int = Field(default_factory=lambda: int(time.time()))
    model: str
    usage: Usage
    choices: list[Choice]

    @classmethod
    def from_model_question_answer(cls, model: str, question: str, answer: str) -> Self:
        return cls(
            model=model,
            usage=Usage.from_question_and_answer(question, answer),
            choices=[Choice.from_model_answer(answer)],
        )
