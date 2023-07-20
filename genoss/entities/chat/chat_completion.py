import time
import uuid
from typing import Any, Dict

from genoss.entities.chat.messages import Message


class ChatCompletion:
    class Choice:
        def __init__(
            self, message: Message, finish_reason: str = "stop", index: int = 0
        ):
            self.message = message
            self.finish_reason = finish_reason
            self.index = index

        def to_dict(self) -> Dict[str, Any]:
            return {
                "message": self.message.to_dict(),
                "finish_reason": self.finish_reason,
                "index": self.index,
            }

    class Usage:
        def __init__(
            self, prompt_tokens: int, completion_tokens: int, total_tokens: int
        ):
            self.prompt_tokens = prompt_tokens
            self.completion_tokens = completion_tokens
            self.total_tokens = total_tokens

        def to_dict(self) -> Dict[str, Any]:
            return {
                "prompt_tokens": self.prompt_tokens,
                "completion_tokens": self.completion_tokens,
                "total_tokens": self.total_tokens,
            }

    def __init__(self, model: str, last_messages: list, answer: str):
        self.id = str(uuid.uuid4())
        self.object = "chat.completion"
        self.created = int(time.time())
        self.model = model
        self.usage = self.Usage(
            len(last_messages), len(answer), len(last_messages) + len(answer)
        )
        self.choices = [
            self.Choice(Message(role="assistant", content=answer), "stop", 0)
        ]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "object": self.object,
            "created": self.created,
            "model": self.model,
            "usage": self.usage.to_dict(),
            "choices": [choice.to_dict() for choice in self.choices],
        }
