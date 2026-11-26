Step 5: several servers, and HTTP with a token (Modules 4 and 5)

  python agent.py "Check this week's specials file. What is the soup special, and how much is it?"
                                   (uses the official filesystem server too: needs Node.js)

  Over HTTP, in two terminals (Windows PowerShell: $env:CAFE_MCP_TOKEN="a-long-random-secret"):
  CAFE_MCP_TOKEN=a-long-random-secret python server.py --http
  CAFE_MCP_TOKEN=a-long-random-secret python http_client.py
