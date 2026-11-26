Corner Café MCP server: the code for "Connect AI to Anything with MCP"

  step-1-hello       Module 1: your first MCP server, and the raw JSON-RPC messages
  step-2-tools       Module 2: the café's booking tools and your own MCP client
  step-3-resources   Module 3: resources, prompts and the staff handbook search (the handbook folder)
  step-4-agents      Module 4: a LangGraph agent using MCP tools, and setup for desktop apps
  step-5-http        Modules 4 and 5: several servers at once, and the server over HTTP with a token
  step-6-final       Modules 5 and 6: tests, a README and packaging

Each step has the finished code for its module plus everything before it. Start with the lessons: they say
which files to copy and when.

You need Python 3.10 or newer, Node.js (LTS, for the MCP Inspector and the filesystem server), and Ollama
(https://ollama.com) with nomic-embed-text (the handbook search) and qwen3:4b-instruct (the agent):

  python -m venv .venv
  source .venv/bin/activate          (Windows PowerShell: .venv\Scripts\activate)
  pip install -r step-6-final/requirements.txt
  ollama pull nomic-embed-text
  ollama pull qwen3:4b-instruct

The handbook folder (from step 3) is the search code and documents from "Search Your Documents with AI: RAG in
Depth". Build its index once: cd handbook && python index.py

The model's answers change from run to run, so yours won't match the lessons word for word.
