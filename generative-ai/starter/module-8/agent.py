"""A small agent: it plans its own steps and uses tools until the job is done (or it runs out of steps)."""
import csv
import sys
from pathlib import Path

import ollama

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "module-6"))
from search import search  # noqa: E402

MODEL = sys.argv[1] if len(sys.argv) > 1 else "qwen3:4b-instruct"  # or: python agent.py llama3.2
MAX_STEPS = 6
BOOKINGS = Path(__file__).resolve().parent / "bookings.csv"

FREE_PLACES = {
    ("maths", "monday"): 0, ("maths", "wednesday"): 2, ("maths", "saturday"): 1,
    ("english", "tuesday"): 3, ("english", "thursday"): 0,
    ("science", "wednesday"): 1, ("science", "saturday"): 4,
}


def search_notes(question: str) -> str:
    """Search Brightside Tutoring's notes (prices, policies, subjects, term dates).

    Args:
        question: what to look up

    Returns:
        The most relevant notes
    """
    return "\n\n".join(c["text"] for _, c in search(question, k=2))


def check_free_places(subject: str) -> str:
    """List the days with free small-group places for a subject.

    Args:
        subject: maths, english or science

    Returns:
        Each day for that subject and its free places
    """
    days = [f"{day}: {n} free" for (subj, day), n in FREE_PLACES.items() if subj == subject.lower()]
    return ", ".join(days) or f"No {subject} groups."


def book_trial(student_name: str, subject: str, day: str) -> str:
    """Book a free trial lesson. Only call this for a day that has a free place.

    Args:
        student_name: the student's first name
        subject: maths, english or science
        day: the day of the week

    Returns:
        A confirmation, or why it couldn't be booked
    """
    if FREE_PLACES.get((subject.lower(), day.lower()), 0) < 1:
        return f"Can't book: no free {subject} place on {day}."
    new_file = not BOOKINGS.exists()
    with BOOKINGS.open("a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if new_file:
            writer.writerow(["student", "subject", "day", "type"])
        writer.writerow([student_name, subject.lower(), day.lower(), "free trial"])
    FREE_PLACES[(subject.lower(), day.lower())] -= 1
    return f"Booked a free trial {subject} lesson for {student_name} on {day}."


TOOLS = {f.__name__: f for f in (search_notes, check_free_places, book_trial)}

task = input("Task for the agent: ")
messages = [
    {"role": "system", "content": "You are an assistant for Brightside Tutoring's front desk. "
                                  "Use the tools to finish the task. Check facts and free places "
                                  "before booking. When you're done, reply with a short summary for the parent."},
    {"role": "user", "content": task},
]

for step in range(1, MAX_STEPS + 1):
    response = ollama.chat(model=MODEL, messages=messages, tools=list(TOOLS.values()),
                           options={"temperature": 0})
    message = response["message"]
    messages.append(message)
    if not message.get("tool_calls"):
        print(f"\nDone in {step} steps:\n{message['content']}")
        break
    for call in message["tool_calls"]:
        name, args = call["function"]["name"], call["function"]["arguments"]
        try:
            result = TOOLS[name](**args)
        except Exception as error:  # a wrong tool name or arguments: tell the model, so it can try again
            result = f"Error: {error!r}. Check the tool name and arguments and try again."
        print(f"Step {step}: {name}({args})\n   -> {result[:120]}")
        messages.append({"role": "tool", "content": result, "tool_name": name})
else:
    print(f"\nStopped after {MAX_STEPS} steps without finishing.")
