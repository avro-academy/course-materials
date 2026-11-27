"""Search Brightside's notes by meaning, not by matching words."""
import json
import math
from pathlib import Path

import ollama

from notes import load_chunks

EMBED_MODEL = "nomic-embed-text"
INDEX_FILE = Path(__file__).resolve().parent / "index.json"


def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    return dot / (math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(y * y for y in b)))


def build_index():
    chunks = load_chunks()
    # nomic-embed-text works best with these prefixes
    vectors = ollama.embed(model=EMBED_MODEL,
                           input=["search_document: " + c["text"] for c in chunks])["embeddings"]
    for chunk, vector in zip(chunks, vectors):
        chunk["vector"] = vector
    INDEX_FILE.write_text(json.dumps(chunks), encoding="utf-8")
    return chunks


def load_index():
    if INDEX_FILE.exists():
        return json.loads(INDEX_FILE.read_text(encoding="utf-8"))
    return build_index()


def search(question, k=3):
    chunks = load_index()
    q = ollama.embed(model=EMBED_MODEL, input="search_query: " + question)["embeddings"][0]
    scored = sorted(chunks, key=lambda c: cosine(q, c["vector"]), reverse=True)
    return [(round(cosine(q, c["vector"]), 3), c) for c in scored[:k]]


if __name__ == "__main__":
    build_index()
    while True:
        question = input("\nSearch (or 'quit'): ")
        if question.strip().lower() == "quit":
            break
        for score, chunk in search(question):
            print(f"{score}  {chunk['source']} > {chunk['title']}")
