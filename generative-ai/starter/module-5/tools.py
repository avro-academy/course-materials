"""Tool use: the model asks our code to look things up, then answers with the result."""
import datetime
import sys

import ollama

MODEL = sys.argv[1] if len(sys.argv) > 1 else "qwen3:4b-instruct"  # or: python tools.py llama3.2

# Pretend booking system: free small-group places per subject and day
FREE_PLACES = {
    ("maths", "monday"): 0, ("maths", "wednesday"): 2, ("maths", "saturday"): 1,
    ("english", "tuesday"): 3, ("english", "thursday"): 0,
    ("science", "wednesday"): 1, ("science", "saturday"): 4,
}


def check_free_places(subject: str, day: str) -> str:
    """Check how many free small-group places there are for a subject on a day of the week.

    Args:
        subject: maths, english or science
        day: a day of the week, like wednesday

    Returns:
        How many places are free
    """
    if not isinstance(subject, str) or not isinstance(day, str):
        return "Error: give one subject and one day per call."
    places = FREE_PLACES.get((subject.lower(), day.lower()))
    if places is None:
        return f"There is no {subject} group on {day}."
    return f"{places} free place{'' if places == 1 else 's'} in {subject} on {day}."


def todays_date() -> str:
    """Get today's date and day of the week.

    Returns:
        Today's date, like Monday 1 February 2027
    """
    today = datetime.date.today()
    return f"{today:%A} {today.day} {today:%B %Y}"


TOOLS = {"check_free_places": check_free_places, "todays_date": todays_date}

question = input("Ask about bookings: ")
messages = [
    {"role": "system", "content": "You answer booking questions for Brightside Tutoring. "
                                  "Use the tools to check places; never guess numbers."},
    {"role": "user", "content": question},
]

response = ollama.chat(model=MODEL, messages=messages, tools=list(TOOLS.values()),
                       options={"temperature": 0})

while response["message"].get("tool_calls"):
    messages.append(response["message"])
    for call in response["message"]["tool_calls"]:
        name = call["function"]["name"]
        args = call["function"]["arguments"]
        try:
            result = TOOLS[name](**args)
        except Exception as error:  # a wrong tool name or arguments: tell the model, so it can try again
            result = f"Error: {error!r}. Check the tool name and arguments and try again."
        print(f"[tool] {name}({args}) -> {result}")
        messages.append({"role": "tool", "content": result, "tool_name": name})
    response = ollama.chat(model=MODEL, messages=messages, tools=list(TOOLS.values()),
                           options={"temperature": 0})

print()
print(response["message"]["content"])
