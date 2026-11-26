"""Your first MCP server: one tool.

    npx @modelcontextprotocol/inspector python hello.py     test it in the MCP Inspector
"""
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Hello Café")

HOURS = {"Monday": "7am", "Tuesday": "7am", "Wednesday": "7am", "Thursday": "7am", "Friday": "7am",
         "Saturday": "8am", "Sunday": "8am"}


@mcp.tool()
def opening_time(day: str) -> str:
    """What time Corner Café opens on a day of the week, like Saturday."""
    opens = HOURS.get(day.strip().capitalize())
    if not opens:
        return f"{day!r} isn't a day of the week."
    return f"Corner Café opens at {opens} on {day.strip().capitalize()}."


if __name__ == "__main__":
    mcp.run()
