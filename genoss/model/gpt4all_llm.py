from __future__ import annotations

from typing import Dict

from langchain import PromptTemplate, LLMChain
from langchain.llms import GPT4All
from langchain.embeddings import GPT4AllEmbeddings
import time
from genoss.model.base_genoss_llm import BaseGenossLLM


class Gpt4AllLLM(BaseGenossLLM):
    name: str = "gpt4all"
    description: str = "GPT-4"
    model_path: str = "./model/ggml-gpt4all-j-v1.3-groovy.bin"

    def generate_answer(self, messages: list) -> Dict:
        print("Generating Answer")
        print(messages)
        last_message = messages

        llm = GPT4All(
            model=self.model_path,  # pyright: ignore reportPrivateUsage=none
        )
        prompt_template = "Question from user: {question}?, Answer from bot:"
        llm_chain = LLMChain(
            llm=llm, prompt=PromptTemplate.from_template(prompt_template)
        )
        response_text = llm_chain(last_message)
        print("###################")
        print(response_text)
        answer = response_text["text"]

        # Format the response to match OpenAI's format
        response = {
            "id": "chatcmpl-abc123",  # You might want to generate a unique ID here
            "object": "chat.completion",
            "created": int(time.time()),  # This gets the current Unix timestamp
            "model": "gpt4all",
            "usage": {
                "prompt_tokens": len(last_message),  # This is a simplification
                "completion_tokens": len(answer),  # This is a simplification
                "total_tokens": len(last_message)
                + len(answer),  # This is a simplification
            },
            "choices": [
                {
                    "message": {"role": "assistant", "content": answer},
                    "finish_reason": "stop",  # This might not always be 'stop'
                    "index": 0,
                }
            ],
        }

        return response

    def generate_embedding(self, embedding: str | list[str]):
        gpt4all_embd = GPT4AllEmbeddings()  # pyright: ignore reportPrivateUsage=none
        embedding_to_str = " ".join(embedding)
        return gpt4all_embd.embed_query(embedding_to_str)
