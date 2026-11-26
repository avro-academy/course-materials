"""Search the café's notes by meaning, without asking the model anything.

    python find.py "Can I bring my pup?"
"""
import sys

from knowledge import Knowledge

notes = Knowledge.from_folder("notes")
print(len(notes.chunks), "sections in the notes")
for score, chunk in notes.search(sys.argv[1], k=3):
    heading = chunk.text.splitlines()[1]  # the ## line, under the file's title
    print(f"{score:.3f}  {chunk.source:<24} {heading}")
