"""Study Buddy answers questions about Brightside from its notes, and says where the answer came from."""
import ollama

from search import search

MODEL = "llama3.2"

SYSTEM = """You answer questions from parents and students about Brightside Tutoring.
Use ONLY the notes below. The notes may use different words from the question, so apply
their rules to the person's situation (for example, 2 hours' notice is less than 24 hours).
If the notes don't have the answer, say you don't know and suggest calling (02) 9630 4471.
Keep answers to 3 sentences or fewer.

Notes:
{notes}"""


def answer(question):
    results = search(question, k=3)
    notes = "\n\n".join(f"[{c['source']}]\n{c['text']}" for _, c in results)
    reply = ollama.chat(
        model=MODEL,
        messages=[{"role": "system", "content": SYSTEM.format(notes=notes)},
                  {"role": "user", "content": question}],
        options={"temperature": 0},
    )
    sources = sorted({c["source"] for _, c in results})
    return reply["message"]["content"].strip(), sources


if __name__ == "__main__":
    while True:
        question = input("\nAsk Study Buddy (or 'quit'): ")
        if question.strip().lower() == "quit":
            break
        text, sources = answer(question)
        print(f"\n{text}\n\nSources: {', '.join(sources)}")
