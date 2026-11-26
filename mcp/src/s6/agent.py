"""Café Helper with MCP: a LangGraph agent with tools from two MCP servers, the café's and the official
filesystem server (which needs Node.js; npx downloads it the first time).

python agent.py "Check this week's specials file. What is the soup special, and how much is it?"
"""
import asyncio
import datetime as dt
import os
import sys

from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_ollama import ChatOllama
from langgraph.graph import START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

# Each MCP server the agent can use. Add more and the agent gets their tools too.
SERVERS = {
    "cafe": {"command": sys.executable, "args": ["server.py"], "transport": "stdio"},
    "files": {"command": "npx", "args": ["-y", "@modelcontextprotocol/server-filesystem", "./shared"], "transport": "stdio"},
}

# Only the tools this agent needs: the café's, and reading (not changing) the shared files
ALLOWED = {"booking_times", "request_booking", "search_handbook",
           "list_allowed_directories", "list_directory", "read_text_file"}

RULES = """You are Café Helper for Corner Café in Sydney. Use your tools for every fact about the café:
bookings, the staff handbook, or anything else your tools offer. Answer in two or three short sentences.
Never make up prices, times or other facts.
The café's shared files, like this week's specials, are in the folder """ + os.path.abspath("shared")


def calendar(days=14):
    """The next two weeks of dates, so the model doesn't have to work out "this Saturday" itself."""
    start = dt.date.today()
    dates = [start + dt.timedelta(days=i) for i in range(days)]
    return f"Today is {start:%A} {start}; " + "; ".join(f"{d:%A} {d}" for d in dates[1:]) + "."


async def main(question):
    client = MultiServerMCPClient(SERVERS)
    tools = [t for t in await client.get_tools() if t.name in ALLOWED]  # MCP tools, as LangChain tools
    print("Tools from MCP:", ", ".join(t.name for t in tools))
    llm = ChatOllama(model="qwen3:4b-instruct", temperature=0).bind_tools(tools)

    async def agent(state: MessagesState):
        return {"messages": [await llm.ainvoke([("system", RULES + "\nDates: " + calendar())] + state["messages"])]}

    graph = StateGraph(MessagesState)
    graph.add_node("agent", agent)
    graph.add_node("tools", ToolNode(tools))
    graph.add_edge(START, "agent")
    graph.add_conditional_edges("agent", tools_condition)
    graph.add_edge("tools", "agent")
    app = graph.compile()

    result = await app.ainvoke({"messages": [("user", question)]})
    for message in result["messages"]:
        message.pretty_print()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit('Ask a question, like: python agent.py "What is this week\'s soup special?"')
    asyncio.run(main(" ".join(sys.argv[1:])))
