"""Chat with Café Helper 2.0 in the terminal. Conversations are saved in memory.db, so you can stop
and carry on later: use the same name to pick up where you left off.

    python chat.py sam
"""
import sys

from langgraph.checkpoint.sqlite import SqliteSaver

from agent import build_graph

config = {"configurable": {"thread_id": sys.argv[1] if len(sys.argv) > 1 else "terminal"}}

with SqliteSaver.from_conn_string("memory.db") as memory:
    graph = build_graph(memory)
    while True:
        text = input("You: ")
        if text.strip().lower() in ("quit", "exit"):
            break
        result = graph.invoke({"messages": [("user", text)]}, config)
        print("Bot:", result["messages"][-1].content)
