from __future__ import annotations
from typing import Dict

from langchain import PromptTemplate, LLMChain
from langchain.llms import OpenAIChat
from langchain.embeddings import OpenAIEmbeddings
from genoss.model.base_genoss_llm import BaseGenossLLM
from genoss.chat.chat_completion import ChatCompletion


class OpenAILLM(BaseGenossLLM):
    name: str = "openai"
    description: str = "OpenAI LLM"
    model_path: str = ""

    def generate_answer(self, messages: list) -> Dict:
        print("Generating Answer")
        print(messages)
        last_messages = messages

        llm = OpenAIChat()
        prompt_template = "Question from user: {question}?, Answer from bot:"
        llm_chain = LLMChain(
            llm=llm, prompt=PromptTemplate.from_template(prompt_template)
        )
        response_text = llm_chain(last_messages)
        print("###################")
        print(response_text)
        answer = response_text["text"]
        chat_completion = ChatCompletion(model=self.name, answer=answer, last_messages=last_messages)

        return chat_completion.to_dict()

    def generate_embedding(self, text: str):
        model = OpenAIEmbeddings()
        return model.embed_query(text)
