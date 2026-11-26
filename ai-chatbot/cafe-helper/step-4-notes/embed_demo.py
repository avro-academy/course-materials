"""Turn three sentences into embeddings: lists of numbers that describe their meaning."""
import ollama

texts = ["Can I bring my pup?", "Dogs are welcome at the outside tables.", "We take cards and cash."]
vectors = ollama.embed(model="nomic-embed-text", input=texts)["embeddings"]

print("Numbers in each vector:", len(vectors[0]))
print("The first five for the question:", [round(x, 3) for x in vectors[0][:5]])
