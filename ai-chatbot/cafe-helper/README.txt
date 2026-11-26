CAFÉ HELPER
Avro Academy · Build Your Own AI Chatbot: Understanding and Using LLMs

Café Helper is a chatbot for Corner Café, a pretend café at 12 Example Street,
Sydney. It runs a large language model on your own computer with Ollama, so
it's free and private. Each folder is the finished code for one stage:

  step-1-terminal    Module 3: ask.py, memory.py, chat.py, temperature.py
  step-2-web         Module 4: the chat web app (Flask + JavaScript)
  step-3-streaming   Module 4: replies that stream in, and Café Helper's personality
  step-4-notes       Modules 5 and 6: answers from the café's notes (RAG),
                     tests and a bot checker

Make your own empty cafe-helper folder and type the code yourself; use these
folders to compare.

YOU NEED
  Python 3.10 or newer, and Ollama (ollama.com/download) with two models:
    ollama pull llama3.2
    ollama pull nomic-embed-text      (for step-4-notes)
  Slow computer? Use llama3.2:1b: change MODEL at the top of the code.

SET UP (once, in your project folder)
  python -m venv .venv
  Mac / Linux:        source .venv/bin/activate
  Windows PowerShell: .venv\Scripts\activate
  pip install -r requirements.txt

RUN IT
  python chat.py                      (step-1-terminal)
  flask --app app run --debug         (the web app; open http://127.0.0.1:5000)

STEP-4-NOTES
  notes/                    the café's information, as Markdown files. Edit them
                            and restart the app: no code needed
  knowledge.py              splits the notes into sections and searches them by meaning
  find.py "question"        see which sections a question finds
  all_notes.py "question"   the simple way: every note in the prompt
  embed_demo.py             what an embedding looks like
  check_bot.py              asks every question in test_questions.csv and checks
                            the answers (run it a few times: answers vary)
  python -m pytest -q       8 tests that don't need Ollama

An LLM's answers are a little different every time, so yours won't match the
lessons word for word.
