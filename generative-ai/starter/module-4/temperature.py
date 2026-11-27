"""The same prompt three times at a low and a high temperature."""
import ollama

MODEL = "llama3.2"
prompt = "Suggest a name for a homework club for Year 5 students. Reply with the name only."

for temperature in [0, 1.2]:
    print(f"--- temperature {temperature} ---")
    for _ in range(3):
        reply = ollama.chat(model=MODEL, messages=[{"role": "user", "content": prompt}],
                            options={"temperature": temperature})
        print(reply["message"]["content"].strip())
