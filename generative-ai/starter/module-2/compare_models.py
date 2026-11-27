"""Ask several models the same questions and save the answers to a CSV file to compare."""
import csv
import time

import ollama

MODELS = ["llama3.2", "qwen3:4b-instruct", "gemma3:4b"]

QUESTIONS = [
    "Explain what a fraction is to a Year 4 student, in two sentences.",
    "Two brothers each take 10 small-group lessons at $45 a lesson. Siblings get 10% off. What is the total?",
    "Write a one-line reminder text for a parent about tomorrow's 4 pm maths lesson.",
]

with open("model-results.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["model", "question", "answer", "seconds"])
    for model in MODELS:
        for question in QUESTIONS:
            start = time.time()
            response = ollama.chat(model=model, messages=[{"role": "user", "content": question}])
            seconds = round(time.time() - start, 1)
            answer = response["message"]["content"].strip()
            writer.writerow([model, question, answer, seconds])
            print(f"{model} ({seconds}s): {answer[:70]}...")

print("Saved model-results.csv")
