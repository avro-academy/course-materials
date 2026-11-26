"""Search the café's notes by meaning, using embeddings from Ollama.

Each note file is split into sections (a line starting with ## starts a new one). Every section is turned
into an embedding: a list of numbers describing what it's about. A question gets an embedding too, and the
sections whose numbers are closest to it are the ones most likely to answer it.
"""
import math
import os
from dataclasses import dataclass, field

import ollama

EMBED_MODEL = "nomic-embed-text"


@dataclass
class Chunk:
    source: str                       # the file it came from, like menu.md
    text: str                         # the section, starting with the file's title
    vector: list = field(default=None, repr=False)


def split_notes(name, text):
    """Split one note file into sections. Each section starts with the file's # title, for context."""
    title, sections, current = name, [], []
    for line in text.strip().splitlines():
        if line.startswith("# "):
            title = line[2:].strip()
        elif line.startswith("## "):
            if "".join(current).strip():
                sections.append(current)
            current = [line]
        else:
            current.append(line)
    if "".join(current).strip():
        sections.append(current)
    return [Chunk(name, title + "\n" + "\n".join(lines).strip()) for lines in sections]


def embed(texts):
    """Turn a list of texts into a list of embeddings (lists of numbers)."""
    return ollama.embed(model=EMBED_MODEL, input=texts)["embeddings"]


def cosine(a, b):
    """How similar two embeddings are: 1 = pointing the same way, 0 = unrelated."""
    dot = sum(x * y for x, y in zip(a, b))
    return dot / (math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(y * y for y in b)))


class Knowledge:
    def __init__(self, chunks, embed=embed):
        self.chunks = chunks
        self.embed = embed
        # nomic-embed-text works best when it's told which texts are documents and which are questions
        vectors = embed(["search_document: " + c.text for c in chunks])
        for chunk, vector in zip(chunks, vectors):
            chunk.vector = vector

    @classmethod
    def from_folder(cls, folder, embed=embed):
        chunks = []
        for name in sorted(os.listdir(folder)):
            if name.endswith(".md"):
                with open(os.path.join(folder, name), encoding="utf-8") as f:
                    chunks += split_notes(name, f.read())
        return cls(chunks, embed)

    def search(self, question, k=3):
        """The k sections most similar to the question, best first, as (score, chunk) pairs."""
        q = self.embed(["search_query: " + question])[0]
        scored = [(cosine(q, chunk.vector), chunk) for chunk in self.chunks]
        scored.sort(key=lambda pair: pair[0], reverse=True)
        return scored[:k]
