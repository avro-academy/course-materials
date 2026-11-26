"""Ask a large language model one question, using Ollama on this computer."""
import ollama

response = ollama.chat(
    model="llama3.2",
    messages=[{"role": "user", "content": "Suggest three names for a new café in Sydney."}],
)
print(response["message"]["content"])

print("Tokens in:", response["prompt_eval_count"])
print("Tokens out:", response["eval_count"])
print("Seconds:", round(response["total_duration"] / 1e9, 1))
