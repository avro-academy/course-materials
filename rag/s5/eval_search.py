"""Score each search method on questions.csv: how often a right section is in the top 1, 3 and 5 results (hit@k),
and the mean reciprocal rank (MRR: 1 for first place, 1/2 for second, 1/3 for third…).

python eval_search.py
"""
import csv

from search import METHODS

with open("questions.csv", newline="", encoding="utf-8") as f:
    QUESTIONS = list(csv.DictReader(f))


def rank_of_right_answer(results, expected):
    """1 if a right section is first, 2 if second…; None if it isn't in the results at all."""
    right = [tuple(part.strip().split(" > ", 1)) for part in expected.split("|")]
    for rank, r in enumerate(results, start=1):
        if (r["source"], r["section"]) in right:
            return rank
    return None


if __name__ == "__main__":
    print(f"{len(QUESTIONS)} questions\n")
    print(f"{'method':<8}  hit@1  hit@3  hit@5   MRR")
    misses = {}
    for name, search in METHODS.items():
        ranks = [rank_of_right_answer(search(q["question"], k=5), q["expected"]) for q in QUESTIONS]
        hit = lambda k: sum(1 for r in ranks if r and r <= k) / len(ranks)
        mrr = sum(1 / r for r in ranks if r) / len(ranks)
        print(f"{name:<8}  {hit(1):>5.0%}  {hit(3):>5.0%}  {hit(5):>5.0%}  {mrr:>5.2f}")
        misses[name] = [q["question"] for q, r in zip(QUESTIONS, ranks) if not r or r > 3]

    for name, questions in misses.items():
        print(f"\nNot in the top 3 with {name}:")
        for q in questions:
            print("  -", q)
