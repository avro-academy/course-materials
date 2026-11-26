"""The tools Café Helper can use. The docstrings and type hints are what the model reads to decide
when to use each tool and what to pass it, so they're written for the model as much as for people."""
import os

from langchain_core.tools import tool

import bookings
from knowledge import Knowledge

_notes = None


def get_notes():
    """The café's notes, split into sections and embedded the first time they're needed."""
    global _notes
    if _notes is None:
        _notes = Knowledge.from_folder(os.path.join(os.path.dirname(os.path.abspath(__file__)), "notes"))
    return _notes


@tool
def search_notes(question: str) -> str:
    """Search Corner Café's notes: menu and prices, opening hours, allergies and diets, visiting, dogs,
    parking, payments, catering and gift cards. Use it for any question about the café."""
    found = get_notes().search(question, k=3)
    return "\n\n".join(f"[{chunk.source}]\n{chunk.text}" for score, chunk in found)


@tool
def booking_times(date: str, people: int, time: str = "") -> str:
    """Check free tables at Corner Café. date is YYYY-MM-DD; people is how many people (1 to 8);
    time is the time the customer asked for, as HH:MM (like 09:30), or empty if they didn't say."""
    problem = bookings.problem_with(date, people)
    if problem:
        return problem
    times = bookings.free_times(date, people)
    if not times:
        return f"Sorry, there are no free times on {date} for {people}."
    free = "Free times that day: " + ", ".join(times) + "."
    if not time:
        return free
    if time in times:
        return f"Yes: {time} on {date} is free for {people}."
    if time not in bookings.TIMES:
        return f"{time} isn't a booking time (bookings are 08:00 to 13:00, every half hour). {free}"
    # Say it plainly: small models miss a time that's simply left out of a list
    return f"No: {time} on {date} is FULL for {people}. {free}"


TOOLS = [search_notes, booking_times]
