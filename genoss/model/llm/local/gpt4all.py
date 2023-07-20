from __future__ import annotations
from tkinter.messagebox import QUESTION

from typing import Dict

from langchain import LLMChain
from langchain.embeddings import GPT4AllEmbeddings
from langchain.llms import GPT4All

from genoss.entities.chat.chat_completion import ChatCompletion
from genoss.model.llm.local.base_local import BaseLocalLLM
from genoss.model.prompts.prompt_template import prompt_template


class Gpt4AllLLM(BaseLocalLLM):
    name: str = "gpt4all"
    description: str = "GPT-4"
    model_path: str = "./local_models/ggml-gpt4all-j-v1.3-groovy.bin"

    def generate_answer(self, question: str) -> Dict:
        print("Generating Answer")

        llm = GPT4All(
            model=self.model_path,  # pyright: ignore reportPrivateUsage=none
        )

        llm_chain = LLMChain(llm=llm, prompt=prompt_template)
        response_text = llm_chain(QUESTION)
        print("###################")
        print(response_text)
        answer = response_text["text"]
        # TODO: fix, chat completion expects a list but message is a string...
        chat_completion = ChatCompletion(
            model=self.name, question=question, answer=answer
        )

        return chat_completion.to_dict()

    def generate_embedding(self, embedding: str | list[str]):
        gpt4all_embd = GPT4AllEmbeddings()  # pyright: ignore reportPrivateUsage=none
        embedding_to_str = " ".join(embedding)
        return gpt4all_embd.embed_query(embedding_to_str)
