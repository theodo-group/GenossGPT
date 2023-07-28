from __future__ import annotations

from typing import TYPE_CHECKING, Any

from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.schema import ChatMessage
from pydantic import Field

from genoss.entities.chat.chat_completion import ChatCompletion
from genoss.llm.base_genoss import BaseGenossLLM

if TYPE_CHECKING:
    from langchain.schema import BaseMessage

    from genoss.entities.chat.message import Message


class OpenAILLM(BaseGenossLLM):
    name: str = "openai"
    description: str = "OpenAI LLM"
    model_name: str = Field("gpt-3.5-turbo", description="OpenAI model name")
    api_key: str

    def _parseMessagesAsChatMessage(self, messages: list[Message]) -> list[BaseMessage]:
        new_messages: list[BaseMessage] = []
        for message in messages:
            new_messages.append(ChatMessage(content=message.content, role=message.role))
        return new_messages

    def generate_answer(self, messages: list[Message]) -> dict[str, Any]:
        llm = ChatOpenAI(model_name=self.model_name, openai_api_key=self.api_key)

        chatMessages = self._parseMessagesAsChatMessage(messages)
        response = llm(chatMessages)

        question = messages[-1].content
        answer = response.content

        chat_completion = ChatCompletion(
            model=self.name, answer=answer, question=question
        )

        return chat_completion.to_dict()

    def generate_embedding(self, text: str) -> list[float]:
        model = OpenAIEmbeddings()
        return model.embed_query(text)
