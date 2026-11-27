"""Check Study Buddy's answers against facts we know are right."""
from rag import answer

TESTS = [
    ("How much is a one-on-one lesson?", ["85"]),
    ("Do you charge an enrolment fee?", ["no enrolment fee", "no fee", "there is no", "don't charge"]),
    ("When does term 2 start in 2027?", ["26 april"]),
    ("Who teaches chemistry?", ["okafor"]),
    ("What happens if we cancel with only 2 hours' notice?", ["can't", "cannot", "not be"]),
    ("Do you teach physics?", ["don't", "do not", "not"]),
    ("Can I pay with Bitcoin?", ["9630 4471", "don't know", "not sure"]),
    ("Are you open on Fridays?", ["closed", "not open"]),
]

passed = 0
for question, any_of in TESTS:
    text, sources = answer(question)
    ok = any(word in text.lower() for word in any_of)
    passed += ok
    print(f"{'PASS' if ok else 'FAIL'}  {question}\n      {text[:110]}")
    if not ok:
        print(f"      Sources: {', '.join(sources)}")

print(f"\n{passed} of {len(TESTS)} passed")
