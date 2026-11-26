"""A workflow: the model sorts each message into a kind, and the graph sends it down a different path.

    python router.py
"""
from typing import Literal

from langchain_ollama import ChatOllama
from langgraph.graph import END, START, MessagesState, StateGraph
from pydantic import BaseModel, Field

llm = ChatOllama(model="qwen3:4b-instruct", temperature=0)


class Kind(BaseModel):
    """What the customer's message is about."""
    kind: Literal["question", "booking", "complaint", "other"] = Field(
        description="question = about the café, menu or hours; booking = wants a table; "
                    "complaint = unhappy about something; other = not about the café")


classifier = llm.with_structured_output(Kind)  # the model must answer with this exact shape


class State(MessagesState):
    kind: str


def classify(state: State):
    result = classifier.invoke([("system", "Sort the customer's message for Corner Café."), state["messages"][-1]])
    return {"kind": result.kind}


def answer_question(state: State):
    reply = llm.invoke([("system", "You are Café Helper for Corner Café. Answer in one short sentence.")] + state["messages"])
    return {"messages": [reply]}


def booking(state: State):
    return {"messages": [("ai", "I'd love to help you book. (Bookings arrive in Module 3!)")]}


def complaint(state: State):
    return {"messages": [("ai", "I'm sorry to hear that. I've passed this to a staff member, who'll follow up.")]}


def other(state: State):
    return {"messages": [("ai", "Sorry, I can only help with questions about Corner Café.")]}


graph = StateGraph(State)
graph.add_node("classify", classify)
for name, step in [("answer_question", answer_question), ("booking", booking), ("complaint", complaint), ("other", other)]:
    graph.add_node(name, step)
    graph.add_edge(name, END)
graph.add_edge(START, "classify")
graph.add_conditional_edges("classify", lambda state: state["kind"],
                            {"question": "answer_question", "booking": "booking", "complaint": "complaint", "other": "other"})
app = graph.compile()

if __name__ == "__main__":
    for text in ["What's in a chai latte?", "Can I get a table for 4 on Saturday?",
                 "My toastie was cold and the staff ignored me.", "Can you do my maths homework?"]:
        result = app.invoke({"messages": [("user", text)]})
        print(f"{text}\n  -> {result['kind']}: {result['messages'][-1].content}")
