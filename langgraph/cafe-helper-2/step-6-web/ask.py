"""Ask Café Helper 2.0 one question and print every message the graph made: the question, any tool
calls and their results, and the answer.

    python ask.py "Is the veggie wrap vegan?"

The tools that ask staff or hand over need a conversation (thread) ID, and pausing for staff needs a
checkpointer, so this uses an in-memory one. (To answer staff questions, use chat.py.)
"""
import sys

from langgraph.checkpoint.memory import InMemorySaver

from agent import build_graph

graph = build_graph(InMemorySaver())
config = {"configurable": {"thread_id": "ask"}}
result = graph.invoke({"messages": [("user", sys.argv[1])]}, config)
for message in result["messages"]:
    message.pretty_print()
if "__interrupt__" in result:
    print("\n(Waiting for staff to confirm:", result["__interrupt__"][0].value, ")")
