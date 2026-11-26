Handbook Assistant: the code for "Search Your Documents with AI: RAG in Depth"

A question-answering assistant for the staff documents of Corner Café (a made-up café): it loads PDFs, Word
and Markdown files, splits them into chunks, searches them by meaning and by keywords, and answers with
citations, using local models in Ollama.

  step-1-load      Module 1: getting the text out of documents
  step-2-chunk     Module 2: chunks and metadata
  step-3-index     Module 3: a vector database (Chroma) and meaning search
  step-4-hybrid    Module 4: keyword search (BM25), hybrid search and measuring search
  step-5-answers   Module 5: answers with citations, and checking them
  step-6-web       Module 6: the web app
  make-docs        how the café's documents were made, so you can change and rebuild them

Each step has the finished code for its module plus everything before it, and its own docs folder.
Start with the lessons: they say which files to copy and when.

You need Python 3.10 or newer, and Ollama (https://ollama.com) with two models:
  ollama pull nomic-embed-text
  ollama pull qwen3:4b-instruct

In each step folder:
  python -m venv .venv
  source .venv/bin/activate          (Windows PowerShell: .venv\Scripts\activate)
  pip install pypdf python-docx chromadb ollama rank-bm25 flask pytest

The model's wording changes from run to run, so your answers won't match the lessons word for word.
