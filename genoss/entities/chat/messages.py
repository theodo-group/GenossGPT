from typing import Any, Dict, List

from pydantic import BaseModel, Field


class Message(BaseModel):
    role: str = Field(
        ...,
        description="The role of the messages author. One of system, user, assistant, or function.",
    )
    content: str = Field(
        ...,
        description="The contents of the message. content is required for all messages, and may be null for assistant messages with function calls.",
    )

    def to_dict(self) -> Dict[str, Any]:
        return {"role": self.role, "content": self.content}


class Messages(BaseModel):
    messages: List[Message]

    def to_dict(self) -> List[Dict[str, Any]]:
        return [message.to_dict() for message in self.messages]

    def __getitem__(self, index):
        return self.messages[index]
