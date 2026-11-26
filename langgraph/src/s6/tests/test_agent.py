"""Tests for Café Helper 2.0's code. A fake model gives scripted replies, so they don't need Ollama.

    python -m pytest -q
"""
import datetime as dt
import os

import pytest
from langchain_core.messages import AIMessage
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command

import app as web
import bookings
from agent import build_graph, calendar


def next_wednesday():
    day = dt.date.today() + dt.timedelta(days=7)
    while day.weekday() != 2 or day.strftime("%m-%d") in bookings.CLOSED:
        day += dt.timedelta(days=1)
    return day.isoformat()


DAY = next_wednesday()


class FakeModel:
    """Stands in for the LLM: each call returns the next scripted reply."""
    def __init__(self, *replies):
        self.replies = list(replies)
        self.seen = []

    def bind_tools(self, tools):
        return self

    def invoke(self, messages):
        self.seen.append(messages)
        return self.replies.pop(0)


def call(tool, **args):
    """A scripted reply asking for a tool, the way the model would."""
    return AIMessage("", tool_calls=[{"name": tool, "args": args, "id": f"call-{tool}"}])


def run(model, text, thread="t1"):
    graph = build_graph(InMemorySaver(), model=model)
    config = {"configurable": {"thread_id": thread}}
    return graph, config, graph.invoke({"messages": [("user", text)]}, config)


@pytest.fixture(autouse=True)
def empty_database():
    if os.path.exists(bookings.DB):
        os.remove(bookings.DB)


def test_problem_with_checks_every_detail():
    assert bookings.problem_with(DAY, 2, "09:30") is None
    assert "isn't a date" in bookings.problem_with("next tuesday", 2)
    assert "past" in bookings.problem_with("2020-01-01", 2)
    assert "1 to 8 people" in bookings.problem_with(DAY, 12)
    assert "isn't a booking time" in bookings.problem_with(DAY, 2, "03:00")


def test_free_times_counts_the_seats():
    assert len(bookings.free_times(DAY, 2)) == 11
    bookings.add_booking("A", DAY, "10:00", 8)
    bookings.add_booking("B", DAY, "10:00", 8)
    assert "10:00" in bookings.free_times(DAY, 4)        # 16 + 4 = 20 seats: just fits
    assert "10:00" not in bookings.free_times(DAY, 5)


def test_calendar_gives_the_next_two_weeks():
    text = calendar()
    assert text.startswith(f"Today is {dt.date.today():%A} {dt.date.today()}")
    assert text.count(";") == 13


def test_agent_loop_runs_the_tool_and_answers():
    model = FakeModel(call("booking_times", date=DAY, people=2, time="09:30"), AIMessage("Yes, 9:30 is free."))
    graph, config, result = run(model, "Table for 2 at 9:30?")
    assert [type(m).__name__ for m in result["messages"]] == ["HumanMessage", "AIMessage", "ToolMessage", "AIMessage"]
    assert result["messages"][2].content == f"Yes: 09:30 on {DAY} is free for 2."
    assert "Dates: Today is" in model.seen[0][0].content   # the rules and calendar go first


def test_a_booking_waits_for_staff_then_is_confirmed():
    model = FakeModel(call("request_booking", name="Priya", date=DAY, time="09:30", people=3),
                      AIMessage("You're booked!"))
    graph, config, result = run(model, "Book 9:30 for 3, I'm Priya")
    assert "__interrupt__" in result                      # stopped, waiting for staff
    assert result["__interrupt__"][0].value["name"] == "Priya"
    [req] = bookings.waiting_requests()
    assert (req["name"], req["time"], req["thread_id"]) == ("Priya", "09:30", "t1")

    result = graph.invoke(Command(resume={"approved": True}), config)
    assert "Confirmed by staff" in result["messages"][-2].content
    assert result["messages"][-1].content == "You're booked!"
    assert "09:30" not in bookings.free_times(DAY, 18)  # 3 booked + 18 would be more than 20 seats
    assert bookings.waiting_requests() == []  # the answer is recorded, so it's off the staff list


def test_a_declined_booking_is_not_added():
    model = FakeModel(call("request_booking", name="Sam", date=DAY, time="11:00", people=2),
                      AIMessage("Sorry, staff couldn't confirm it."))
    graph, config, result = run(model, "Book 11 for 2, I'm Sam")
    result = graph.invoke(Command(resume={"approved": False, "note": "Private event"}), config)
    assert "Private event" in result["messages"][-2].content
    assert bookings.bookings_on(DAY) == []


def test_hand_over_is_saved_for_staff():
    model = FakeModel(call("hand_over_to_staff", reason="complaint", summary="Cold coffee"),
                      AIMessage("A staff member will follow up."))
    run(model, "My coffee was cold!", thread="unhappy")
    [handover] = bookings.open_handovers()
    assert (handover["reason"], handover["thread_id"]) == ("complaint", "unhappy")


def test_each_thread_has_its_own_memory():
    graph = build_graph(InMemorySaver(), model=FakeModel(AIMessage("Hi Sam"), AIMessage("Hi Priya"), AIMessage("Sam!")))
    sam, priya = ({"configurable": {"thread_id": t}} for t in ("sam", "priya"))
    graph.invoke({"messages": [("user", "I'm Sam")]}, sam)
    graph.invoke({"messages": [("user", "I'm Priya")]}, priya)
    graph.invoke({"messages": [("user", "Who am I?")]}, sam)
    assert len(graph.get_state(sam).values["messages"]) == 4
    assert len(graph.get_state(priya).values["messages"]) == 2


@pytest.fixture
def client(monkeypatch):
    monkeypatch.setattr(web, "STAFF_PASSWORD", "letmein")
    return web.app.test_client()


def login(client):
    client.get("/staff")
    with client.session_transaction() as s:
        token = s["csrf"]
    client.post("/staff/login", data={"password": "letmein", "csrf": token})
    return token


def test_staff_pages_need_the_password(client, monkeypatch):
    assert client.get("/staff/chat/abc").status_code == 403
    with client.session_transaction() as s:
        s["csrf"] = "x"
    assert client.post("/staff/login", data={"password": "wrong", "csrf": "x"}).status_code == 401
    monkeypatch.setattr(web, "STAFF_PASSWORD", "")
    assert client.get("/staff").status_code == 404           # no password set: no staff pages at all


def test_staff_confirm_needs_csrf_and_resumes_the_customer(client, monkeypatch):
    model = FakeModel(call("request_booking", name="Priya", date=DAY, time="09:30", people=3), AIMessage("You're booked!"))
    monkeypatch.setattr(web, "graph", build_graph(InMemorySaver(), model=model))
    client.post("/api/chat", json={"message": "Book 9:30 for 3, I'm Priya"})
    [req] = bookings.waiting_requests()
    token = login(client)
    assert client.post(f"/staff/requests/{req['id']}", data={"action": "approve"}).status_code == 400  # no token
    client.post(f"/staff/requests/{req['id']}", data={"action": "approve", "csrf": token})
    assert bookings.get_request(req["id"])["status"] == "approved"
    assert len(bookings.bookings_on(DAY)) == 1


def test_customer_cannot_chat_while_booking_waits(client, monkeypatch):
    model = FakeModel(call("request_booking", name="Priya", date=DAY, time="09:30", people=3))
    monkeypatch.setattr(web, "graph", build_graph(InMemorySaver(), model=model))
    data = client.post("/api/chat", json={"message": "Book 9:30 for 3, I'm Priya"}).get_json()
    assert data["waiting"] and data["messages"][-1]["text"] == web.WAITING
    assert data["messages"][-1]["tools"] == ["request_booking"]
    assert client.post("/api/chat", json={"message": "Hello?"}).status_code == 409
