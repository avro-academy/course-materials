"""Show every checkpoint saved for one conversation, newest first.   python history.py sam"""
import sys

from langgraph.checkpoint.sqlite import SqliteSaver

from agent import build_graph

config = {"configurable": {"thread_id": sys.argv[1]}}
with SqliteSaver.from_conn_string("memory.db") as memory:
    graph = build_graph(memory)
    for snapshot in graph.get_state_history(config):
        last = snapshot.values["messages"][-1] if snapshot.values.get("messages") else None
        text = " ".join(str(last.content or last.tool_calls).split()) if last else ""
        what = f"{type(last).__name__}: {text[:55]}" if last else "(empty)"
        print(f"step {snapshot.metadata['step']:>2}  next={snapshot.next or '-'}  {what}")
