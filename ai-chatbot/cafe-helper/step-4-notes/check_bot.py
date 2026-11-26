"""Ask Café Helper every question in test_questions.csv and check the answers.

    python check_bot.py

Each row has a question, words the answer should include (any one of them, separated by |)
and words it must not include. LLM answers change from run to run, so run it a few times.
"""
import csv

from app import answer

passed = 0
with open("test_questions.csv", newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

for row in rows:
    reply, sources = answer(row["question"])
    text = reply.lower()
    expect = [w.strip().lower() for w in row["expect"].split("|") if w.strip()]
    avoid = [w.strip().lower() for w in row["avoid"].split("|") if w.strip()]
    ok = (not expect or any(w in text for w in expect)) and not any(w in text for w in avoid)
    passed += ok
    print(("PASS" if ok else "FAIL"), row["question"])
    if not ok:
        print("     answer:", " ".join(reply.split()))

print(f"{passed} of {len(rows)} passed")
