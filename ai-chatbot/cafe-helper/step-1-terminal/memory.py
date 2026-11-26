"""Two separate calls: the second one knows nothing about the first."""
import ollama

first = ollama.chat(model="llama3.2", messages=[
    {"role": "user", "content": "My name is Priya and I work at a café."},
])
print("1:", first["message"]["content"])

second = ollama.chat(model="llama3.2", messages=[
    {"role": "user", "content": "What's my name, and where do I work?"},
])
print("2:", second["message"]["content"])
