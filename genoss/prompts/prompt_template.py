from langchain import PromptTemplate

system_prompt = "Question from user: {question}?, Answer from helpful chatbot:"

prompt_template = PromptTemplate(template=system_prompt, input_variables=["question"])
