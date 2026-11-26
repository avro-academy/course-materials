"""Café Helper — a chatbot web app, using a large language model that runs on your computer with Ollama.

Run it:   flask --app app run --debug
"""
import ollama
from flask import Flask, abort, jsonify, render_template, request

MODEL = "llama3.2"
SYSTEM_PROMPT = "You are a friendly helper. Keep your answers short."
MAX_MESSAGES = 20    # only send the latest messages, so long chats stay fast
MAX_CHARS = 1000     # the longest message we accept

app = Flask(__name__)


def clean_messages(data):
    """The conversation sent by the browser: only user and assistant messages, and not too long."""
    messages = data.get("messages") if isinstance(data, dict) else None
    if not isinstance(messages, list) or not messages:
        abort(400)
    cleaned = []
    for m in messages[-MAX_MESSAGES:]:
        if not isinstance(m, dict) or m.get("role") not in ("user", "assistant") or not isinstance(m.get("content"), str):
            abort(400)
        cleaned.append({"role": m["role"], "content": m["content"][:MAX_CHARS]})
    return cleaned


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/api/chat")
def chat():
    messages = clean_messages(request.get_json(silent=True))
    try:
        response = ollama.chat(model=MODEL, messages=[{"role": "system", "content": SYSTEM_PROMPT}] + messages)
    except ConnectionError:
        return jsonify(error="The AI model isn't available. Is Ollama running?"), 503
    return jsonify(reply=response["message"]["content"])
