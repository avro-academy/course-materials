"""Corner Café's MCP server: tools for bookings and the staff handbook, resources to read, and prompts.

    python seed.py                                           fill this Saturday with some bookings
    cd handbook && python index.py                           build the handbook's search index (once)
    npx @modelcontextprotocol/inspector python server.py     test it in the MCP Inspector
"""
import os
import secrets
import sys

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

import bookings

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "handbook"))  # the search code from the RAG course

mcp = FastMCP("Corner Café", instructions="Information about Corner Café in Sydney: menu, opening hours, "
              "table bookings and the staff handbook.",
              log_level="WARNING")  # log problems only, not every request


# ---------- tools: actions the AI can take ----------

@mcp.tool(annotations=ToolAnnotations(title="Check free tables", readOnlyHint=True))
def booking_times(date: str, people: int, time: str = "") -> str:
    """Check free tables at Corner Café. date is YYYY-MM-DD; people is how many people (1 to 8);
    time is the time asked for, as HH:MM (like 09:30), or empty to list every free time that day."""
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
    return f"No: {time} on {date} is FULL for {people}. {free}"


@mcp.tool(annotations=ToolAnnotations(title="Request a booking", readOnlyHint=False, destructiveHint=False, idempotentHint=False))
def request_booking(name: str, date: str, time: str, people: int) -> str:
    """Ask Corner Café to book a table. It isn't confirmed until staff approve it on the staff page.
    date is YYYY-MM-DD, time is HH:MM (like 09:30). Check booking_times first."""
    problem = bookings.problem_with(date, people, time)
    if problem:
        return problem
    if time not in bookings.free_times(date, people):
        return f"{time} on {date} isn't free for {people}. Check booking_times."
    name = " ".join(name.split())[:60]
    bookings.add_request(f"mcp-{secrets.token_hex(6)}", "mcp", name, date, time, people)
    return f"Request sent: {name}, {people} people, {date} at {time}. Staff will confirm it."


@mcp.tool(annotations=ToolAnnotations(title="Search the staff handbook", readOnlyHint=True))
def search_handbook(question: str) -> str:
    """Search Corner Café's staff documents (handbook, food safety, espresso guide, policies, FAQ).
    Returns the 3 best-matching sections, each with its document and page, to answer staff questions."""
    from search import hybrid_search
    results = hybrid_search(question, 3)
    return "\n\n".join(f"[{n}] {c['title']}{', page ' + str(c['page']) if c['page'] else ''} — {c['section']}\n{c['text']}"
                       for n, c in enumerate(results, start=1))


# ---------- resources: information an app can read ----------

def read(name):
    with open(os.path.join(HERE, name), encoding="utf-8") as f:
        return f.read()


@mcp.resource("cafe://menu", mime_type="text/markdown")
def menu() -> str:
    """Corner Café's menu and prices."""
    return read("menu.md")


@mcp.resource("cafe://hours", mime_type="text/markdown")
def hours() -> str:
    """Opening hours, including public holidays."""
    return read("hours.md")


@mcp.resource("cafe://bookings/{date}", mime_type="text/plain")
def day_bookings(date: str) -> str:
    """How full each booking time is on a date (YYYY-MM-DD): seats taken, out of 20."""
    problem = bookings.problem_with(date, 1)
    if problem:
        return problem
    return "\n".join(f"{t}  {taken:>2} of {bookings.SEATS_PER_TIME} seats booked" for t, taken in bookings.seats_taken(date).items())


# ---------- prompts: ready-made instructions a person can pick ----------

@mcp.prompt(title="Reply to a customer")
def reply_to_customer(message: str) -> str:
    """Draft a friendly reply to a customer's email or message."""
    return ("You're replying for Corner Café, 12 Example Street, Sydney. Write a short, warm reply in Australian English "
            "to the customer message below. Use the café's tools and resources for any facts (menu, hours, bookings); "
            "never make up prices or times. Sign off as 'The Corner Café team'.\n\nCustomer message:\n" + message)


@mcp.prompt(title="New staff welcome")
def new_staff_welcome(name: str, role: str = "barista") -> str:
    """Write a welcome message for a new team member, from the staff handbook."""
    return (f"Write a short welcome message for {name}, who is starting at Corner Café as a {role}. Use search_handbook "
            "to include: when the roster comes out, pay day, what to wear, and who to call if they're sick.")


if __name__ == "__main__":
    mcp.run()
