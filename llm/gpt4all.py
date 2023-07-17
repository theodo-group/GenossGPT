from classes.llm import LLM
from langchain.llms.gpt4all import GPT4All
from langchain import PromptTemplate, LLMChain
from langchain.llms import GPT4All


class gpt_4_all(LLM):
    name: str = "gpt4all"
    description: str = "GPT-4"
    model_path: str = "./llm/ggml-gpt4all-j-v1.3-groovy.bin"

    def generate_answer(self, question: str) -> str:
        llm = GPT4All(
            model=self.model_path,
        )  # pyright: ignore reportPrivateUsage=none
        prompt_template = "Question from user: {question}?, Answer from bot:"
        llm_chain = LLMChain(
            llm=llm, prompt=PromptTemplate.from_template(prompt_template)
        )
        response = llm_chain(question)
        return response["text"]

    def generate_embedding(self, prompt: str):
        return [0.0, 0.0, 0.0]
