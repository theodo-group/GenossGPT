from langchain.embeddings import GPT4AllEmbeddings
from langchain.llms import GPT4All

from genoss.entities.chat.chat_completion import ChatCompletion
from genoss.entities.chat.message import Message
from genoss.llm.local.base_local import BaseLocalLLM


class Gpt4AllLLM(BaseLocalLLM):
    name: str = "gpt4all"
    description: str = "GPT4ALL"
    model_path: str = "./local_models/ggml-gpt4all-j-v1.3-groovy.bin"

    def generate_answer(self, messages: list[Message]) -> ChatCompletion:
        llm = GPT4All(
            model=self.model_path,  # pyright: ignore reportPrivateUsage=none
        )
        return self._chat_completion_from_langchain_llm(llm=llm, messages=messages)

    def generate_embedding(self, embedding: str | list[str]) -> list[float]:
        gpt4all_embd = GPT4AllEmbeddings()  # pyright: ignore reportPrivateUsage=none
        embedding_to_str = " ".join(embedding)
        return gpt4all_embd.embed_query(embedding_to_str)
