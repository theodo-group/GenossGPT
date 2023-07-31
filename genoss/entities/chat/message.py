from typing import Any, Literal

from pydantic import BaseModel, Field

MessageRole = Literal["system", "user", "assistant", "function"]


class Message(BaseModel):
    role: MessageRole = Field(
        ...,
        description="The role of the messages author. One of system, user, assistant, or function.",
    )
    content: str = Field(
        ...,
        description="The contents of the message. content is required for all messages, and may be null for assistant messages with function calls.",
    )

    def to_dict(self) -> dict[str, Any]:
        return {"role": self.role, "content": self.content}
