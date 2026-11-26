"""The same question three times at a low temperature, and three times at a high one."""
import ollama

question = [{"role": "user", "content": "Suggest one name for a café. Answer with just the name."}]

for temperature in (0, 1.5):
    print("Temperature", temperature)
    for _ in range(3):
        response = ollama.chat(model="llama3.2", messages=question, options={"temperature": temperature})
        print("  ", response["message"]["content"])
