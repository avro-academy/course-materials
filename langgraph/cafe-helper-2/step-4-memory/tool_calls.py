"""What the model does with tools it's been given: it answers, or replies with tool calls. It never runs them.

    python tool_calls.py
"""
from langchain_ollama import ChatOllama

from tools import booking_times, search_notes

llm = ChatOllama(model="qwen3:4b-instruct", temperature=0).bind_tools([search_notes, booking_times])

print(booking_times.args_schema.model_json_schema())  # what the model is told about booking_times
for question in ["Is the toastie vegetarian?", "Any tables for 2 on 2026-12-24?", "Hello!"]:
    reply = llm.invoke(question)
    print(question, "->", reply.tool_calls or reply.content)
