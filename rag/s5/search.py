"""Step 4: three ways to search — by meaning (vector), by words (keyword, BM25), and both at once (hybrid).

python search.py "FSS-208841"                        (hybrid, the default)
python search.py "How long do I get for lunch?" --method keyword
python search.py "When is pay day?" --all-versions   (include replaced documents too)
"""
import re
import sys

from rank_bm25 import BM25Okapi

from index import embed, get_collection


def vector_search(question, k=5, current_only=True):
    """Chunks whose meaning is closest to the question. Old documents are left out unless current_only=False."""
    where = {"current": True} if current_only else None
    found = get_collection().query(query_embeddings=embed([question], "search_query"), n_results=k, where=where)
    return [{"id": i, "text": t, "score": 1 - d, **m}
            for i, t, d, m in zip(found["ids"][0], found["documents"][0], found["distances"][0], found["metadatas"][0])]


# Very common words say nothing about what a question is about, so keyword search ignores them
STOP_WORDS = set("""a an and are as at be but by can do does for from get go got have how i if in is it its me my
of on or our so than that the their them then there they this to up us was we what when where which who why will
with you your""".split())


def words(text):
    """Lowercase words for keyword search, without punctuation or stop words."""
    return [w for w in re.findall(r"[a-z0-9$%°]+(?:[.'][a-z0-9]+)*", text.lower()) if w not in STOP_WORDS]


_bm25 = None


def keyword_index(current_only=True):
    global _bm25
    if _bm25 is None or _bm25[0] != current_only:
        everything = get_collection().get(where={"current": True} if current_only else None)
        chunks = [{"id": i, "text": t, **m} for i, t, m in zip(everything["ids"], everything["documents"], everything["metadatas"])]
        _bm25 = (current_only, chunks, BM25Okapi([words(c["text"]) for c in chunks]))
    return _bm25[1], _bm25[2]


def keyword_search(question, k=5, current_only=True):
    """Chunks that share the most (and the rarest) words with the question: BM25, the classic search-engine score."""
    chunks, bm25 = keyword_index(current_only)
    scores = bm25.get_scores(words(question))
    best = sorted(range(len(chunks)), key=lambda i: scores[i], reverse=True)[:k]
    return [{**chunks[i], "score": float(scores[i])} for i in best if scores[i] > 0]


def hybrid_search(question, k=5, current_only=True):
    """Both searches, combined with Reciprocal Rank Fusion: a chunk scores 1/(60 + its rank) in each list."""
    fused = {}
    for results in (vector_search(question, 20, current_only), keyword_search(question, 20, current_only)):
        for rank, chunk in enumerate(results, start=1):
            entry = fused.setdefault(chunk["id"], {**chunk, "score": 0.0})
            entry["score"] += 1 / (60 + rank)
    return sorted(fused.values(), key=lambda c: c["score"], reverse=True)[:k]


METHODS = {"vector": vector_search, "keyword": keyword_search, "hybrid": hybrid_search}


def show(results):
    for r in results:
        where = r["source"] + (f" p{r['page']}" if r["page"] else "")
        print(f"{r['score']:.3f}  {where:<41}  {' '.join(r['text'].split())[:70]}")


if __name__ == "__main__":
    args, method = [], "hybrid"
    rest = iter(sys.argv[1:])
    for a in rest:
        if a == "--method":
            method = next(rest, "hybrid")
        elif not a.startswith("--"):
            args.append(a)
    if not args or method not in METHODS:
        sys.exit('Ask a question, like: python search.py "When is pay day?" [--method vector|keyword|hybrid] [--all-versions]')
    show(METHODS[method](" ".join(args), k=3, current_only="--all-versions" not in sys.argv))
