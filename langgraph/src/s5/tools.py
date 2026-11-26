"""The tools Café Helper can use. The docstrings and type hints are what the model reads to decide
when to use each tool and what to pass it, so they're written for the model as much as for people."""
import os
from typing import Annotated

from langchain_core.runnables import RunnableConfig
from langchain_core.tools import InjectedToolCallId, tool
from langgraph.types import interrupt

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


@tool
def request_booking(name: str, date: str, time: str, people: int,
                    config: RunnableConfig, tool_call_id: Annotated[str, InjectedToolCallId]) -> str:
    """Ask the café staff to confirm a table booking. Only use it after booking_times shows the time is free
    AND the customer has told you their name. date is YYYY-MM-DD, time is HH:MM (like 09:30)."""
    problem = bookings.problem_with(date, people, time)
    if problem:
        return problem
    if time not in bookings.free_times(date, people):
        return f"{time} on {date} is no longer free. Check booking_times again."
    thread_id = config["configurable"]["thread_id"]
    bookings.add_request(tool_call_id, thread_id, name, date, time, people)

    # Stop here until a staff member answers. The answer comes back from interrupt().
    decision = interrupt({"type": "booking", "name": name, "date": date, "time": time, "people": people})

    bookings.answer_request(tool_call_id, "approved" if decision.get("approved") else "declined")
    if decision.get("approved"):
        booking_id = bookings.add_booking(name, date, time, people)
        return f"Confirmed by staff: booking #{booking_id} for {name}, {people} people, {date} at {time}."
    return f"Staff could not confirm the booking. Their note: {decision.get('note') or 'none'}"


@tool
def hand_over_to_staff(reason: str, summary: str, config: RunnableConfig) -> str:
    """Pass the conversation to a staff member. Use it for complaints, serious allergies, anything about
    someone's safety or money, groups of more than 8, or when the customer asks for a person.
    reason is a few words; summary says what the customer needs and how to contact them, if they said."""
    handover_id = bookings.add_handover(config["configurable"]["thread_id"], reason, summary)
    return f"Handed over to staff (#{handover_id}). Tell the customer a staff member will follow up soon."


TOOLS = [search_notes, booking_times, request_booking, hand_over_to_staff]
