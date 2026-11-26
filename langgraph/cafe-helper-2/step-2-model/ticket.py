"""Your first LangGraph graph, with no AI yet. An order goes through two steps, like a ticket in a café kitchen.

    python ticket.py
"""
from typing import TypedDict

from langgraph.graph import END, START, StateGraph

PRICES = {"flat white": 4.80, "banana bread": 5.50, "veggie wrap": 11.00}


class Order(TypedDict):
    """The state: everything the steps know about the order. Each step reads it and adds to it."""
    items: list[str]
    total: float
    ticket: str


def add_prices(order: Order):
    return {"total": round(sum(PRICES[item] for item in order["items"]), 2)}


def write_ticket(order: Order):
    lines = [f"  {item:<14} ${PRICES[item]:.2f}" for item in order["items"]]
    return {"ticket": "ORDER\n" + "\n".join(lines) + f"\n  {'TOTAL':<14} ${order['total']:.2f}"}


graph = StateGraph(Order)
graph.add_node("add_prices", add_prices)
graph.add_node("write_ticket", write_ticket)
graph.add_edge(START, "add_prices")
graph.add_edge("add_prices", "write_ticket")
graph.add_edge("write_ticket", END)
app = graph.compile()

if __name__ == "__main__":
    result = app.invoke({"items": ["flat white", "banana bread"]})
    print(result["ticket"])
    print()
    print(result)
