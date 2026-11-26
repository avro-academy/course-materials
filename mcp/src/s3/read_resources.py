import asyncio
import datetime
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

today = datetime.date.today()
saturday = (today + datetime.timedelta(days=(5 - today.weekday()) % 7 or 7)).isoformat()


async def main():
    async with stdio_client(StdioServerParameters(command=sys.executable, args=["server.py"])) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            for uri in ["cafe://menu", f"cafe://bookings/{saturday}"]:
                result = await session.read_resource(uri)
                print(f"--- {uri}\n{result.contents[0].text[:400]}\n")


asyncio.run(main())
