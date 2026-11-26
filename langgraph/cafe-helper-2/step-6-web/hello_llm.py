"""Talk to the model through LangChain's ChatOllama, which LangGraph uses.

    python hello_llm.py
"""
from langchain_ollama import ChatOllama

llm = ChatOllama(model="qwen3:4b-instruct", temperature=0)
reply = llm.invoke([
    ("system", "You are a friendly helper at a Sydney café. Answer in one sentence."),
    ("user", "What's a flat white?"),
])
print(type(reply).__name__)
print(reply.content)
print(reply.usage_metadata)
