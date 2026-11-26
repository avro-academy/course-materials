CAFÉ HELPER 2.0
Avro Academy · AI Agents with LangGraph: Café Helper 2.0

Café Helper 2.0 is an AI agent for Corner Café, a pretend café at 12 Example
Street, Sydney. It answers from the café's notes, checks free tables, asks
staff to confirm bookings and hands complaints to a person. It runs on your
own computer with Ollama. Each folder is the finished code after one module,
and has everything from the folders before it:

  step-1-graphs      Module 1: ticket.py, milk.py (graphs with no AI)
  step-2-model       Module 2: hello_llm.py, chat_graph.py, router.py
  step-3-tools       Module 3: notes/, knowledge.py, bookings.py, seed.py,
                     tools.py, agent.py, ask.py, tool_calls.py
  step-4-memory      Module 4: memory_demo.py, chat.py, history.py
  step-5-approval    Module 5: bookings wait for staff; handovers
  step-6-web         Modules 5 and 6: the web app with a staff page, tests
                     and check_agent.py

Make your own cafe-helper-2 folder and type the code yourself; use these
folders to compare.

YOU NEED
  Python 3.10 or newer, and Ollama (ollama.com/download) with two models:
    ollama pull qwen3:4b-instruct
    ollama pull nomic-embed-text

SET UP (once, in your project folder)
  python -m venv .venv
  Mac / Linux:        source .venv/bin/activate
  Windows PowerShell: .venv\Scripts\activate
  pip install -r requirements.txt

TRY IT
  python seed.py                         some bookings for the coming Saturday
  python ask.py "Is the veggie wrap vegan?"
  python chat.py sam                     a conversation that's saved in memory.db
  python history.py sam                  every step of that conversation

THE WEB APP (step-6-web)
  Mac / Linux:        STAFF_PASSWORD=choose-a-password flask --app app run --debug
  Windows PowerShell: $env:STAFF_PASSWORD="choose-a-password"; flask --app app run --debug
  Open http://127.0.0.1:5000 to chat, and http://127.0.0.1:5000/staff for staff.

TESTS AND CHECKS (step-6-web)
  python -m pytest -q       11 tests with a fake model: no Ollama needed
  python check_agent.py     typical conversations with the real model

Bookings are kept in bookings.db and conversations in memory.db. Delete them
to start again. The model's answers are a little different every time, so
yours won't match the lessons word for word.
