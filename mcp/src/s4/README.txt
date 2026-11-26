Step 4: an agent with MCP tools (Module 4)

  pip install langchain-mcp-adapters langgraph langchain-ollama
  ollama pull qwen3:4b-instruct
  python agent.py "Is there a table for 4 this Saturday at 10am?"
  python agent.py "What do I need to wear for my first shift?"

  Desktop apps: see claude_desktop_config.example.json and .vscode/mcp.json (change the paths to yours).
