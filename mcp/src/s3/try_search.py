import asyncio
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    async with stdio_client(StdioServerParameters(command=sys.executable, args=["server.py"])) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool("search_handbook", {"question": "What do I do if I'm sick?"})
            print(result.content[0].text[:700])


asyncio.run(main())
