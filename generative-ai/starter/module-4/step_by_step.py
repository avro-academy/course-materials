"""Ask for the working, then check it yourself."""
import ollama

MODEL = "llama3.2"

question = (
    "Brightside charges $45 for a small-group lesson. Siblings get 10% off when both "
    "are enrolled. Two sisters each take 10 lessons. What is the total?"
)

prompts = {
    "Answer only": question + " Reply with the number only.",
    "Step by step": question + " Work it out step by step, then give the total on the last line.",
}

for name, prompt in prompts.items():
    reply = ollama.chat(model=MODEL, messages=[{"role": "user", "content": prompt}],
                        options={"temperature": 0})
    print(f"--- {name} ---")
    print(reply["message"]["content"].strip())

print("--- Checked by Python ---")
print(2 * 10 * 45 * 0.9)
