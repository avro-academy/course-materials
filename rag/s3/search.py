"""Step 3: search the vector database by meaning.

python search.py "How long do I get for lunch?"
python search.py "When is pay day?" --all-versions     (include replaced documents too)
"""
import sys

from index import embed, get_collection


def vector_search(question, k=5, current_only=True):
    """Chunks whose meaning is closest to the question. Old documents are left out unless current_only=False."""
    where = {"current": True} if current_only else None
    found = get_collection().query(query_embeddings=embed([question], "search_query"), n_results=k, where=where)
    return [{"id": i, "text": t, "score": 1 - d, **m}
            for i, t, d, m in zip(found["ids"][0], found["documents"][0], found["distances"][0], found["metadatas"][0])]


def show(results):
    for r in results:
        where = r["source"] + (f" p{r['page']}" if r["page"] else "")
        print(f"{r['score']:.3f}  {where:<41}  {' '.join(r['text'].split())[:70]}")


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        sys.exit('Ask a question, like: python search.py "When is pay day?"')
    show(vector_search(" ".join(args), k=3, current_only="--all-versions" not in sys.argv))
