Step 6: the web app (Module 6)

  pip install -r requirements.txt
  flask --app app run --debug      then open http://127.0.0.1:5000
                                   (the first start builds the index if there isn't one)
  python -m pytest                 tests for loading, chunking and the web app (no Ollama needed)
