"""Café Helper 2.0 on the web: customers chat with the agent; staff confirm bookings and read handovers.

    STAFF_PASSWORD=choose-a-password flask --app app run --debug

Without STAFF_PASSWORD, the staff pages don't exist.
"""
import os
import secrets
import sqlite3

from flask import Flask, abort, jsonify, redirect, render_template, request, session, url_for
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.types import Command

import bookings
from agent import build_graph

MAX_CHARS = 1000
WAITING = "I've sent your booking to our staff to confirm. I'll tell you here as soon as they answer."

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or secrets.token_hex(32)
STAFF_PASSWORD = os.environ.get("STAFF_PASSWORD", "")

memory = SqliteSaver(sqlite3.connect(os.environ.get("MEMORY_DB", os.path.join(app.root_path, "memory.db")),
                                     check_same_thread=False))
graph = build_graph(memory)


def customer_config():
    """Each browser gets its own conversation (thread), remembered in its session cookie."""
    if "thread_id" not in session:
        session["thread_id"] = secrets.token_hex(8)
    return {"configurable": {"thread_id": session["thread_id"]}}


def conversation(config):
    """What the customer should see: their messages and the agent's answers, not the tool calls.
    Each answer also lists the tools the agent used for it (the 🔧 line)."""
    state = graph.get_state(config)
    shown, tools = [], []
    for m in state.values.get("messages", []):
        if isinstance(m, HumanMessage):
            shown.append({"role": "user", "text": m.content})
            tools = []
        elif isinstance(m, AIMessage):
            tools += [call["name"] for call in m.tool_calls]
            if m.content:
                shown.append({"role": "bot", "text": m.content, "tools": tools})
                tools = []
    # Waiting for staff, or staff have answered and the agent is still writing its reply
    waiting = bool(state.interrupts or state.next)
    if waiting:
        shown.append({"role": "bot", "text": WAITING, "tools": tools})
    return shown, waiting


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/api/chat")
def get_chat():
    shown, waiting = conversation(customer_config())
    return jsonify(messages=shown, waiting=waiting)


@app.post("/api/chat")
def chat():
    data = request.get_json(silent=True)
    text = data.get("message") if isinstance(data, dict) else None
    if not isinstance(text, str) or not text.strip():
        abort(400)
    config = customer_config()
    state = graph.get_state(config)
    if state.interrupts or state.next:
        return jsonify(error="Please wait: staff are still looking at your booking."), 409
    try:
        graph.invoke({"messages": [("user", text.strip()[:MAX_CHARS])]}, {**config, "recursion_limit": 12})
    except ConnectionError:
        return jsonify(error="The AI model isn't available. Is Ollama running?"), 503
    shown, waiting = conversation(config)
    return jsonify(messages=shown, waiting=waiting)


# ---- Staff pages ----

def csrf_token():
    if "csrf" not in session:
        session["csrf"] = secrets.token_hex(16)
    return session["csrf"]


app.jinja_env.globals["csrf_token"] = csrf_token


def staff_only():
    """Staff pages exist only when STAFF_PASSWORD is set, and need a login. Forms need the CSRF token."""
    if not STAFF_PASSWORD:
        abort(404)
    if not session.get("staff"):
        abort(403)
    if request.method == "POST" and not secrets.compare_digest(request.form.get("csrf", ""), session.get("csrf", "")):
        abort(400)


@app.get("/staff")
def staff():
    if not STAFF_PASSWORD:
        abort(404)
    if not session.get("staff"):
        return render_template("login.html")
    return render_template("staff.html", requests=bookings.waiting_requests(), handovers=bookings.open_handovers())


@app.post("/staff/login")
def staff_login():
    if not STAFF_PASSWORD:
        abort(404)
    if not secrets.compare_digest(request.form.get("csrf", ""), session.get("csrf", "")):
        abort(400)
    if secrets.compare_digest(request.form.get("password", "").encode(), STAFF_PASSWORD.encode()):
        session["staff"] = True
        return redirect(url_for("staff"))
    return render_template("login.html", error="That password isn't right."), 401


@app.post("/staff/logout")
def staff_logout():
    staff_only()
    session.pop("staff", None)
    return redirect(url_for("index"))


@app.post("/staff/requests/<int:request_id>")
def answer_request(request_id):
    staff_only()
    req = bookings.get_request(request_id)
    if not req or req["status"] != "waiting":
        abort(404)
    approved = request.form.get("action") == "approve"
    config = {"configurable": {"thread_id": req["thread_id"]}}
    if graph.get_state(config).interrupts:
        # Carry on from where the agent stopped: interrupt() returns this answer inside request_booking
        graph.invoke(Command(resume={"approved": approved, "note": request.form.get("note", "")[:300]}), config)
    bookings.set_request_status(request_id, "approved" if approved else "declined")
    return redirect(url_for("staff"))


@app.post("/staff/handovers/<int:handover_id>")
def finish_handover(handover_id):
    staff_only()
    bookings.close_handover(handover_id)
    return redirect(url_for("staff"))


@app.get("/staff/chat/<thread_id>")
def staff_chat(thread_id):
    """The whole conversation for staff, tool calls and results included."""
    staff_only()
    lines = []
    for m in graph.get_state({"configurable": {"thread_id": thread_id}}).values.get("messages", []):
        if isinstance(m, HumanMessage):
            lines.append(("Customer", m.content))
        elif isinstance(m, AIMessage):
            for call in m.tool_calls:
                lines.append(("Tool call", f"{call['name']}({', '.join(f'{k}={v!r}' for k, v in call['args'].items())})"))
            if m.content:
                lines.append(("Café Helper", m.content))
        elif isinstance(m, ToolMessage):
            lines.append((f"Result of {m.name}", m.content))
    return render_template("chat_log.html", thread_id=thread_id, lines=lines)
