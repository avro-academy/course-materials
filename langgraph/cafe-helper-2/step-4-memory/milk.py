"""Decisions and loops: a graph that steams milk until it's hot enough, and serves takeaway or dine-in.

    python milk.py
"""
import operator
from typing import Annotated, TypedDict

from langgraph.graph import END, START, StateGraph


class Coffee(TypedDict):
    takeaway: bool
    milk_temp: int
    log: Annotated[list[str], operator.add]  # a reducer: each step's log lines are ADDED, not replaced


def steam_milk(coffee: Coffee):
    temp = coffee["milk_temp"] + 15
    return {"milk_temp": temp, "log": [f"steamed the milk to {temp}°C"]}


def hot_enough(coffee: Coffee):
    """A routing function: looks at the state and says which step comes next."""
    if coffee["milk_temp"] < 60:
        return "steam_milk"  # not yet: go round again
    return "takeaway_cup" if coffee["takeaway"] else "dine_in_cup"


def takeaway_cup(coffee: Coffee):
    return {"log": ["poured it into a takeaway cup with a lid"]}


def dine_in_cup(coffee: Coffee):
    return {"log": ["poured it into a ceramic cup"]}


graph = StateGraph(Coffee)
graph.add_node("steam_milk", steam_milk)
graph.add_node("takeaway_cup", takeaway_cup)
graph.add_node("dine_in_cup", dine_in_cup)
graph.add_edge(START, "steam_milk")
graph.add_conditional_edges("steam_milk", hot_enough, ["steam_milk", "takeaway_cup", "dine_in_cup"])
graph.add_edge("takeaway_cup", END)
graph.add_edge("dine_in_cup", END)
app = graph.compile()

if __name__ == "__main__":
    for takeaway in (True, False):
        result = app.invoke({"takeaway": takeaway, "milk_temp": 20, "log": []})
        print("Takeaway:" if takeaway else "Dine in:")
        for line in result["log"]:
            print("  -", line)
