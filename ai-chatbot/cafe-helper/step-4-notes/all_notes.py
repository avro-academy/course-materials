"""Answer one question with ALL the café's notes in the system prompt."""
import os
import sys

import ollama

notes = ""
for name in sorted(os.listdir("notes")):
    with open(os.path.join("notes", name), encoding="utf-8") as f:
        notes += f.read() + "\n\n"

system = "You are Café Helper for Corner Café. Answer in one or two sentences, using only these notes:\n\n" + notes
response = ollama.chat(model="llama3.2", messages=[
    {"role": "system", "content": system},
    {"role": "user", "content": sys.argv[1]},
])
print(response["message"]["content"])
print("Tokens in:", response["prompt_eval_count"])
