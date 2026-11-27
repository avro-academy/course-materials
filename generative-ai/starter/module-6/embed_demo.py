"""Turn sentences into embeddings and see which ones are close in meaning."""
import math

import ollama

EMBED_MODEL = "nomic-embed-text"


def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    return dot / (math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(y * y for y in b)))


sentences = [
    "How much does a lesson cost?",
    "What are your prices?",
    "Is my child safe with your tutors?",
    "The cat sat on the mat.",
]

vectors = ollama.embed(model=EMBED_MODEL, input=sentences)["embeddings"]
print(f"Each embedding has {len(vectors[0])} numbers. The first five: {[round(x, 3) for x in vectors[0][:5]]}")
print()

for i, sentence in enumerate(sentences[1:], start=1):
    print(f"{cosine(vectors[0], vectors[i]):.3f}  '{sentences[0]}' vs '{sentence}'")
