# Generative AI for Beginners: starter files

Starter files for the free Avro Academy course **Generative AI for Beginners: Understand It, Use It, Build With It** (avro.academy).

## What's here

| Folder or file | Used in |
| --- | --- |
| `data/brightside-notes/` | Brightside Tutoring's notes (a made-up business) for search and RAG, Module 6 |
| `model-test-sheet.csv` | Comparing models, Module 2.4 |
| `module-2/compare_models.py` | Comparing models |
| `module-3/redteam.py`, `redteam_v2.py` | Red-teaming Study Buddy |
| `module-4/` | Few-shot, step by step, temperature, JSON output |
| `module-5/` | First app, lesson-plan template, chat with memory, tool use |
| `module-6/` | Embeddings, search, RAG and answer checks |
| `module-8/agent.py` | The booking agent |

## Set up

1. Install Ollama from ollama.com, then:

   ```
   ollama pull llama3.2
   ollama pull nomic-embed-text
   ollama pull qwen3:4b-instruct
   ollama pull gemma3:4b
   ```

2. In this folder:

   ```
   python -m venv .venv
   source .venv/bin/activate      # Windows PowerShell: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Run a program from its own folder, for example `cd module-5` then `python chat.py`.

Checked with Ollama 0.40.18, the ollama Python library 0.6.3 and Python 3.13. AI replies differ every time, so yours won't match the lessons word for word.

## Licence

This course is adapted from Microsoft's [Generative AI for Beginners](https://github.com/microsoft/generative-ai-for-beginners), used under the MIT licence: see `LICENSE-generative-ai-for-beginners.txt`. Avro Academy is not affiliated with or endorsed by Microsoft.
