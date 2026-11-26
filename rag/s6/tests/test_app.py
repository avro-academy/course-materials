"""Tests for the web app. The search and the model are replaced with fakes, so Ollama doesn't need to be running."""
import os

os.environ["SKIP_INDEX"] = "1"

import pytest

import app as web

CHUNKS = [
    {"source": "Corner-Cafe-Staff-Handbook-2026.pdf", "page": 4, "section": "2.3 Breaks", "title": "Staff Handbook (2026)",
     "updated": "2026-07-01", "text": "2.3 Breaks\nIf you work more than 5 hours, you get a 30-minute unpaid meal break."},
    {"source": "Staff-FAQ.md", "page": 0, "section": "Can I have a coffee on my shift?", "title": "Staff FAQ",
     "updated": "2026-07-01", "text": "Can I have a coffee on my shift?\nYes: one free coffee every shift."},
]


@pytest.fixture
def client():
    return web.app.test_client()


def test_answer_with_only_the_cited_sources(client, monkeypatch):
    monkeypatch.setattr(web, "answer", lambda q: {"answer": "A 30-minute break [1].", "sources": CHUNKS, "cited": [1]})
    data = client.post("/api/ask", json={"question": "How long is my lunch break?"}).get_json()
    assert data["answer"] == "A 30-minute break [1]."
    assert [s["n"] for s in data["sources"]] == [1]
    assert data["sources"][0]["link"] == "/docs/Corner-Cafe-Staff-Handbook-2026.pdf#page=4"
    assert data["sources"][0]["label"] == "Staff Handbook (2026), page 4 — 2.3 Breaks"


def test_markdown_sources_have_no_page(client, monkeypatch):
    monkeypatch.setattr(web, "answer", lambda q: {"answer": "Yes [2].", "sources": CHUNKS, "cited": [2]})
    data = client.post("/api/ask", json={"question": "Free coffee?"}).get_json()
    assert data["sources"][0]["link"] == "/docs/Staff-FAQ.md"


def test_long_questions_are_cut_short(client, monkeypatch):
    asked = []
    monkeypatch.setattr(web, "answer", lambda q: asked.append(q) or {"answer": "", "sources": [], "cited": []})
    client.post("/api/ask", json={"question": "x" * 2000})
    assert len(asked[0]) == web.MAX_CHARS


@pytest.mark.parametrize("body", [{}, {"question": ""}, {"question": "   "}, {"question": 42}, None])
def test_bad_questions_are_refused(client, body):
    assert client.post("/api/ask", json=body).status_code == 400


def test_ollama_not_running(client, monkeypatch):
    def broken(q):
        raise ConnectionError("Failed to connect to Ollama")
    monkeypatch.setattr(web, "answer", broken)
    response = client.post("/api/ask", json={"question": "When is pay day?"})
    assert response.status_code == 503
    assert "Ollama" in response.get_json()["error"]


def test_documents_are_served(client):
    response = client.get("/docs/Staff-FAQ.md")
    assert response.status_code == 200
    assert b"Staff FAQ" in response.data


@pytest.mark.parametrize("path", ["/docs/..%2Fapp.py", "/docs/app.py", "/docs/nothing.pdf", "/docs/../app.py"])
def test_only_documents_in_the_docs_folder(client, path):
    assert client.get(path).status_code == 404
