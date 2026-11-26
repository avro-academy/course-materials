"""Step 3: embed every chunk and store it, with its metadata, in a Chroma vector database (the chroma_db folder).

Run it again whenever the documents change:  python index.py
"""
import os
import time

import chromadb
import ollama

import catalogue
from chunk import chunk_pages
from load import load_documents

EMBED_MODEL = "nomic-embed-text"
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chroma_db")


def embed(texts, kind="search_document"):
    """Embeddings from Ollama. nomic-embed-text wants to know which texts are documents and which are questions."""
    return ollama.embed(model=EMBED_MODEL, input=[f"{kind}: {t}" for t in texts])["embeddings"]


def get_collection():
    client = chromadb.PersistentClient(path=DB_PATH)
    return client.get_or_create_collection("handbook", metadata={"hnsw:space": "cosine"})


def build():
    start = time.time()
    chunks = chunk_pages(load_documents())
    client = chromadb.PersistentClient(path=DB_PATH)
    try:
        client.delete_collection("handbook")  # start fresh, so deleted documents disappear too
    except Exception:
        pass
    collection = get_collection()
    for i in range(0, len(chunks), 32):  # embed in batches
        batch = chunks[i:i + 32]
        collection.add(
            ids=[c["id"] for c in batch],
            documents=[c["text"] for c in batch],
            embeddings=embed([c["text"] for c in batch]),
            metadatas=[{"source": c["source"], "page": c["page"] or 0, "section": c["section"],
                        **catalogue.info(c["source"])} for c in batch],
        )
    print(f"Indexed {collection.count()} chunks from {len({c['source'] for c in chunks})} documents "
          f"in {time.time() - start:.1f} seconds.")


if __name__ == "__main__":
    build()
