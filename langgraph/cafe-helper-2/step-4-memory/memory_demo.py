"""Memory with a checkpointer: each thread ID is its own conversation.

    python memory_demo.py
"""
from langgraph.checkpoint.memory import InMemorySaver

from agent import build_graph

graph = build_graph(InMemorySaver())  # a checkpointer that keeps everything in memory

sam = {"configurable": {"thread_id": "sam"}}
priya = {"configurable": {"thread_id": "priya"}}

graph.invoke({"messages": [("user", "Hi, I'm Sam. I'm vegetarian.")]}, sam)
graph.invoke({"messages": [("user", "Hi, I'm Priya.")]}, priya)

result = graph.invoke({"messages": [("user", "What's my name, and what could I eat?")]}, sam)
print("Sam's thread:", result["messages"][-1].content)

result = graph.invoke({"messages": [("user", "What's my name?")]}, priya)
print("Priya's thread:", result["messages"][-1].content)
print("Messages saved for Sam:", len(graph.get_state(sam).values["messages"]))
