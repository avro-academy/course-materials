Step 3: resources, prompts and the handbook (Module 3)

  pip install pypdf python-docx chromadb ollama rank-bm25
  ollama pull nomic-embed-text
  cd handbook && python index.py && cd ..     build the handbook's search index
  python read_resources.py                    read cafe://menu and one day's bookings
  python get_prompt.py                        fill in the "Reply to a customer" prompt
  python try_search.py                        call search_handbook
