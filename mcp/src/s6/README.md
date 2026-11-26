# Corner Café MCP server

An [MCP](https://modelcontextprotocol.io) server for Corner Café, a (made-up) café in Sydney. Any MCP app —
Claude Desktop, VS Code, your own agent — can check free tables, request bookings and search the staff handbook.

## What it offers

| Kind | Name | What it does | Changes things? |
|---|---|---|---|
| Tool | `booking_times` | Free tables on a date, for a number of people | No (read only) |
| Tool | `request_booking` | Asks for a booking; staff confirm it | Adds a request; never books directly |
| Tool | `search_handbook` | The 3 best sections of the staff documents | No (read only) |
| Resource | `cafe://menu`, `cafe://hours` | The menu and opening hours | — |
| Resource template | `cafe://bookings/{date}` | How full each booking time is | — |
| Prompt | `reply_to_customer`, `new_staff_welcome` | Ready-made instructions | — |

## What it needs

- Python 3.10 or newer: `pip install -r requirements.txt`
- [Ollama](https://ollama.com) with `nomic-embed-text` for `search_handbook` (and `qwen3:4b-instruct` for `agent.py`)
- Build the handbook index once: `cd handbook && python index.py`
- Optional: `python seed.py` adds sample bookings for this Saturday

## Settings

| Variable | Used for |
|---|---|
| `CAFE_MCP_TOKEN` | The secret every HTTP request must send as `Authorization: Bearer …`. Required with `--http` |
| `BOOKINGS_DB` | Where the bookings database lives (default: `bookings.db` next to the code) |

## Run it

- In an app (stdio): the app starts `python server.py` itself. See below.
- Over HTTP: `CAFE_MCP_TOKEN=a-long-random-secret python server.py --http` → `http://127.0.0.1:8000/mcp`.
  Put it behind HTTPS before anyone else uses it.
- Test it: `npx @modelcontextprotocol/inspector python server.py`, and `python -m pytest -q`

### Claude Desktop

Settings → Developer → Edit Config, then add (with your own paths):

```json
{
  "mcpServers": {
    "corner-cafe": {
      "command": "/Users/sam/cafe-mcp/.venv/bin/python",
      "args": ["/Users/sam/cafe-mcp/server.py"]
    }
  }
}
```

### VS Code

`.vscode/mcp.json` in the project:

```json
{
  "servers": {
    "corner-cafe": {
      "type": "stdio",
      "command": "${workspaceFolder}/.venv/bin/python",
      "args": ["${workspaceFolder}/server.py"]
    }
  }
}
```

## Versions

Apps depend on the tool names and schemas above. New features are added as new tools; changing an existing
tool is a new major version.
