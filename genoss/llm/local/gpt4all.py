from __future__ import annotations

from typing import Any

from langchain import LLMChain
from langchain.embeddings import GPT4AllEmbeddings
from langchain.llms import GPT4All

from genoss.entities.chat.chat_completion import ChatCompletion
from genoss.entities.chat.message import Message
from genoss.llm.local.base_local import BaseLocalLLM
from genoss.prompts.prompt_template import prompt_template


class Gpt4AllLLM(BaseLocalLLM):
    name: str = "gpt4all"
    description: str = "GPT-4"
    model_path: str = "./local_models/ggml-gpt4all-j-v1.3-groovy.bin"

    def generate_answer(self, messages: list[Message]) -> dict[str, Any]:
        llm = GPT4All(
            model=self.model_path,  # pyright: ignore reportPrivateUsage=none
        )

        llm_chain = LLMChain(llm=llm, prompt=prompt_template)

        question = messages[-1].content
        response_text = llm_chain(question)

        answer = response_text["text"]

        chat_completion = ChatCompletion(
            model=self.name, question=question, answer=answer
        )

        return chat_completion.to_dict()

    def generate_embedding(self, embedding: str | list[str]) -> list[float]:
        gpt4all_embd = GPT4AllEmbeddings()  # pyright: ignore reportPrivateUsage=none
        embedding_to_str = " ".join(embedding)
        return gpt4all_embd.embed_query(embedding_to_str)
