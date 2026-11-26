"""Talk to an MCP server with raw JSON-RPC messages over stdio, to see what's really sent."""
import json
import subprocess
import sys

server = subprocess.Popen([sys.executable, "hello.py"], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                          stderr=subprocess.DEVNULL, text=True)  # hide the server's log messages


def send(message):
    server.stdin.write(json.dumps(message) + "\n")
    server.stdin.flush()
    if "id" in message:  # requests get a reply; notifications don't
        reply = json.loads(server.stdout.readline())
        print(json.dumps(reply, indent=1)[:600], "\n")


send({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {
    "protocolVersion": "2025-06-18", "capabilities": {}, "clientInfo": {"name": "by-hand", "version": "1"}}})
send({"jsonrpc": "2.0", "method": "notifications/initialized"})
send({"jsonrpc": "2.0", "id": 2, "method": "tools/list"})
send({"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "opening_time", "arguments": {"day": "Sunday"}}})
server.terminate()
