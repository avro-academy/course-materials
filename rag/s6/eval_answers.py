"""Check the whole pipeline: for every question in questions.csv, does the answer contain the key fact, and does it
cite a place where that fact really is? And for questions the documents can't answer, does it say so?
It takes a few minutes. python eval_answers.py
"""
import csv

from ask import NOT_FOUND, answer

UNANSWERABLE = ["Can I bring my dog to work?", "Is there staff parking?", "What's the café's Instagram account?"]

with open("questions.csv", newline="", encoding="utf-8") as f:
    QUESTIONS = list(csv.DictReader(f))

passed = 0
for q in QUESTIONS:
    result = answer(q["question"])
    right = [tuple(part.strip().split(" > ", 1)) for part in q["expected"].split("|")]
    cited = [result["sources"][n - 1] for n in result["cited"]]
    has_fact = q["answer"].lower() in result["answer"].lower()
    cites_right = any((c["source"], c["section"]) in right for c in cited)
    ok = has_fact and cites_right
    passed += ok
    if not ok:
        problem = "no citation to the right place" if has_fact else f"missing '{q['answer']}'"
        print(f"FAIL {q['question']}  ({problem})")
        print("     ", " ".join(result["answer"].split()))

for question in UNANSWERABLE:
    result = answer(question)
    ok = NOT_FOUND.lower()[:25] in result["answer"].lower()
    passed += ok
    if not ok:
        print(f"FAIL {question}  (should say it couldn't find it)")
        print("     ", " ".join(result["answer"].split()))

print(f"{passed} of {len(QUESTIONS) + len(UNANSWERABLE)} passed")
