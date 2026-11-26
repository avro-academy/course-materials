"""Corner Café's MCP server: tools for table bookings.

    python seed.py                                           fill this Saturday with some bookings
    npx @modelcontextprotocol/inspector python server.py     test it in the MCP Inspector
"""
import secrets

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

import bookings

mcp = FastMCP("Corner Café", instructions="Information about Corner Café in Sydney: table bookings.",
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


if __name__ == "__main__":
    mcp.run()
