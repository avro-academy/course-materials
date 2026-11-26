"""Your own MCP client: start the café server, see what it offers, and call a tool.

python client.py
"""
import asyncio
import datetime
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# The app starts the server itself, as a separate program, and talks to it over stdin/stdout
SERVER = StdioServerParameters(command=sys.executable, args=["server.py"])

today = datetime.date.today()
SATURDAY = (today + datetime.timedelta(days=(5 - today.weekday()) % 7 or 7)).isoformat()


async def main():
    async with stdio_client(SERVER) as (read, write):
        async with ClientSession(read, write) as session:
            info = await session.initialize()
            print("Connected to:", info.serverInfo.name)

            for tool in (await session.list_tools()).tools:
                print("tool:    ", tool.name, "-", tool.description.split(".")[0])

            print("\nCalling booking_times for Saturday", SATURDAY)
            result = await session.call_tool("booking_times", {"date": SATURDAY, "people": 4, "time": "10:00"})
            print(result.content[0].text)


asyncio.run(main())
