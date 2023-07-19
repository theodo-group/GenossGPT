from __future__ import annotations
import uuid
from typing import Dict

from langchain import PromptTemplate, LLMChain
from langchain.llms import FakeListLLM
from langchain.embeddings import GPT4AllEmbeddings, FakeEmbeddings
import time
from genoss.model.base_genoss_llm import BaseGenossLLM


class FakeLLM(BaseGenossLLM):
    name: str = "fake"
    description: str = "Fake LLM for testing purpose"
    model_path: str = ""

    def generate_answer(self, messages: list) -> Dict:
        print("Generating Answer")
        print(messages)
        last_message = messages

        llm = FakeListLLM(responses=["Hello from FakeLLM!"])
        prompt_template = "Question from user: {question}?, Answer from bot:"
        llm_chain = LLMChain(
            llm=llm, prompt=PromptTemplate.from_template(prompt_template)
        )
        response_text = llm_chain(last_message)
        print("###################")
        print(response_text)
        answer = response_text["text"]

        # Format the response to match OpenAI's format
        unique_id = uuid.uuid4()
        response = {
            "id": unique_id,  # You might want to generate a unique ID here
            "object": "chat.completion",
            "created": int(time.time()),  # This gets the current Unix timestamp
            "model": self.name,
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

    def generate_embedding(self, text: str):
        model = FakeEmbeddings()
        return model.embed_query(text)
