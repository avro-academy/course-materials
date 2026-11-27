"""Zero-shot vs few-shot: show the model examples of the answer you want."""
import ollama

MODEL = "llama3.2"

zero_shot = "Sort this parent message into a category: 'Can Mia move to Thursdays next term?'"

few_shot = """Sort each parent message into one category: BOOKING, BILLING, COMPLAINT or OTHER.
Answer with the category only.

Message: How much is a term of one-on-one English?
Category: BILLING

Message: The tutor was 20 minutes late again today.
Category: COMPLAINT

Message: Can Mia move to Thursdays next term?
Category:"""

for name, prompt in [("Zero-shot", zero_shot), ("Few-shot", few_shot)]:
    reply = ollama.chat(model=MODEL, messages=[{"role": "user", "content": prompt}])
    print(f"--- {name} ---")
    print(reply["message"]["content"].strip())
