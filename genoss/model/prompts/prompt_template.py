from langchain import PromptTemplate

system_prompt = "Question from user: {question}?, Answer from bot:"

prompt_template = PromptTemplate.from_template(system_prompt)
