from __future__ import annotations

from typing import Dict, Optional

from langchain import LLMChain
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms import OpenAIChat
from pydantic import Field

from genoss.entities.chat.chat_completion import ChatCompletion
from genoss.llm.base_genoss import BaseGenossLLM
from genoss.prompts.prompt_template import prompt_template


class OpenAILLM(BaseGenossLLM):
    name: str = "openai"
    description: str = "OpenAI LLM"
    model_name: str = Field("gpt-3.5-turbo", description="OpenAI model name")
    openai_api_key: Optional[str] = Field(None)

    def __init__(self, model_name: str, api_key, *args, **kwargs):
        super().__init__(name=self.name, description=self.description, *args, **kwargs)

        if api_key is None:
            raise ValueError("API key missing")

        self.openai_api_key = api_key
        self.model_name = model_name

    def generate_answer(self, question: str) -> Dict:
        print("Generating Answer")

        llm = OpenAIChat(model=self.model_name, openai_api_key=self.openai_api_key)

        llm_chain = LLMChain(llm=llm, prompt=prompt_template)
        response_text = llm_chain(question)

        print("###################")
        print(response_text)

        answer = response_text["text"]
        chat_completion = ChatCompletion(
            model=self.name, answer=answer, question=question
        )

        return chat_completion.to_dict()

    def generate_embedding(self, text: str):
        model = OpenAIEmbeddings()
        return model.embed_query(text)
