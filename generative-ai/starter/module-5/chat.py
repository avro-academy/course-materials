"""Study Buddy in the terminal: a chat that remembers the conversation."""
import ollama

MODEL = "llama3.2"

SYSTEM = """You are Study Buddy, a friendly homework helper for students at Brightside Tutoring.
- Help students understand; don't just give the final answer to homework questions.
  Give a hint or the first step, then ask them to try.
- Keep replies short: 4 sentences or fewer unless the student asks for more.
- Use simple words and Australian spelling.
- If you aren't sure something is right, say so."""

messages = [{"role": "system", "content": SYSTEM}]
print("Study Buddy is ready. Type 'quit' to stop.\n")

while True:
    question = input("You: ")
    if question.strip().lower() == "quit":
        break
    messages.append({"role": "user", "content": question})
    reply = ollama.chat(model=MODEL, messages=messages)
    answer = reply["message"]["content"]
    messages.append({"role": "assistant", "content": answer})
    print(f"\nStudy Buddy: {answer}\n")
