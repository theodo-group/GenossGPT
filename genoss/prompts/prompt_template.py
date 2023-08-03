from langchain import PromptTemplate

system_prompt = """\
    You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe. Answer in the language of the question \
    Here is the question from the user: {question}\
    Answer:\
"""

prompt_template = PromptTemplate(template=system_prompt, input_variables=["question"])
