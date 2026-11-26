from chunk import fixed_chunks
from load import load_documents

page = [p for p in load_documents() if p["source"].startswith("Corner-Cafe-Staff-Handbook-2026") and p["page"] == 4][0]
for n, piece in enumerate(fixed_chunks(page["text"], size=60, overlap=10), start=1):
    print(f"--- chunk {n}: {piece[:85]}…{piece[-45:]}")
