"""Connect to the café server over HTTP, with the token, and search the handbook.

    CAFE_MCP_TOKEN=a-long-random-secret python http_client.py    (with the server running: python server.py --http)
"""
import asyncio
import os

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

URL = "http://127.0.0.1:8000/mcp"
HEADERS = {"Authorization": f"Bearer {os.environ.get('CAFE_MCP_TOKEN', '')}"}


async def main():
    async with streamablehttp_client(URL, headers=HEADERS) as (read, write, _):
        async with ClientSession(read, write) as session:
            info = await session.initialize()
            print("Connected over HTTP to:", info.serverInfo.name)
            result = await session.call_tool("search_handbook", {"question": "When is pay day?"})
            print(result.content[0].text[:300])


asyncio.run(main())
