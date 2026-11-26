"""Step 6: the Staff Handbook Assistant, as a web app.

pip install -r requirements.txt
flask --app app run --debug        then open http://127.0.0.1:5000
"""
import os

from flask import Flask, abort, jsonify, render_template, request, send_from_directory

from ask import answer, source_label
from index import build, get_collection
from load import DOCS

MAX_CHARS = 500  # a longer question is cut short: nobody needs more, and it keeps prompts small

app = Flask(__name__)


@app.get("/")
def home():
    return render_template("index.html")


@app.post("/api/ask")
def ask():
    question = (request.get_json(silent=True) or {}).get("question")
    if not isinstance(question, str) or not question.strip():
        abort(400)
    try:
        result = answer(question.strip()[:MAX_CHARS])
    except ConnectionError:
        return jsonify(error="The AI model isn't available. Is Ollama running?"), 503
    sources = []
    for n in result["cited"]:
        chunk = result["sources"][n - 1]
        link = f"/docs/{chunk['source']}" + (f"#page={chunk['page']}" if chunk.get("page") else "")
        sources.append({"n": n, "label": source_label(chunk), "link": link, "excerpt": " ".join(chunk["text"].split())[:400]})
    return jsonify(answer=result["answer"], sources=sources)


@app.get("/docs/<name>")
def document(name):
    """The original documents, so staff can check a source. Only files that are really in the docs folder."""
    if name not in os.listdir(DOCS):
        abort(404)
    return send_from_directory(DOCS, name)


if os.environ.get("SKIP_INDEX") != "1" and get_collection().count() == 0:
    build()  # the first time the app starts, build the index
