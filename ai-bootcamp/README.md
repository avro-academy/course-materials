Avro AI Starter, rebuilt from the AI App Bootcamp lessons (weeks 0–2) after the original file was lost.

- Engine and model match the site's /device-check page: WebLLM 0.2.86 with `gemma3-1b-it-q4f16_1-MLC`.
- WebLLM 0.2.86 has no 32-bit Gemma 3, so WebGPU without shader-f16 uses `Qwen2.5-0.5B-Instruct-q4f32_1-MLC`. (The device-check page still says such devices get "a bigger download, about 860 MB".)
- No WebGPU: Transformers.js 3.5.1 with `HuggingFaceTB/SmolLM2-360M-Instruct` (q8, about 370 MB) on the processor, in a worker.
- `?engine=mock` gives pretend replies; `?engine=backup` forces the processor AI.

Tested in headless Chromium: every tab in test mode; chat, FAQ and summariser end to end with the backup AI; the WebLLM path loads and streams on software WebGPU. Gemma itself needs a real graphics chip with 16-bit support, so it wasn't run here.
