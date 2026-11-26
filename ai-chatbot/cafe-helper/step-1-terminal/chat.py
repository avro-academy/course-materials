"""A chatbot in the terminal. Type a message and press Enter; type quit to stop."""
import ollama

MODEL = "llama3.2"

# The whole conversation so far. The model doesn't remember anything itself,
# so every turn sends all of it again.
messages = [
    {"role": "system", "content": "You are a friendly helper. Keep your answers short."},
]

while True:
    question = input("You: ")
    if question.strip().lower() in ("quit", "exit"):
        break
    messages.append({"role": "user", "content": question})

    print("Bot: ", end="", flush=True)
    reply = ""
    for chunk in ollama.chat(model=MODEL, messages=messages, stream=True):
        piece = chunk["message"]["content"]
        print(piece, end="", flush=True)  # show each piece as soon as it arrives
        reply += piece
    print()

    messages.append({"role": "assistant", "content": reply})
