Step 3: a vector database (Module 3)

  pip install chromadb ollama
  ollama pull nomic-embed-text
  python index.py                                   embed every chunk into the chroma_db folder
  python search.py "How long do I get for lunch?"   search by meaning
  python search.py "When is pay day?" --all-versions
