"""Ask Café Helper 2.0 one question and print every message the graph made: the question, any tool
calls and their results, and the answer.

    python ask.py "Is the veggie wrap vegan?"
"""
import sys

from agent import build_graph

graph = build_graph()
result = graph.invoke({"messages": [("user", sys.argv[1])]})
for message in result["messages"]:
    message.pretty_print()
