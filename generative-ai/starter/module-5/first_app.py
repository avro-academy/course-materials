"""Your first text-generation program: one prompt in, one answer out."""
import ollama

MODEL = "llama3.2"

topic = input("What should the quiz question be about? ")

response = ollama.chat(
    model=MODEL,
    messages=[{"role": "user", "content": f"Write one multiple-choice quiz question about {topic} "
                                          "for a Year 6 student, with four options and the answer."}],
)
print()
print(response["message"]["content"])
