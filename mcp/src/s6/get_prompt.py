import asyncio
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    async with stdio_client(StdioServerParameters(command=sys.executable, args=["server.py"])) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            prompt = await session.get_prompt("reply_to_customer", {"message": "Hi, are you open on Anzac Day? Thanks, Jo"})
            for message in prompt.messages:
                print(message.role, ":", message.content.text)


asyncio.run(main())
