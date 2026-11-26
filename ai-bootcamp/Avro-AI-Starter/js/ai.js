// js/ai.js: loads the AI and gets replies from it.
// Three engines, picked automatically:
//   Gemma 3 1B (WebLLM, runs on the graphics chip with WebGPU)  - the main AI
//   Qwen2.5 0.5B (WebLLM, 32-bit)                              - graphics chips without 16-bit support
//   SmolLM2 360M (Transformers.js, runs on the processor)      - backup when there's no WebGPU
//   mock (?engine=mock in the address)                         - pretend replies for testing
// You don't need to change this file.

const WEBLLM_URL = "https://cdn.jsdelivr.net/npm/@mlc-ai/web-llm@0.2.86/+esm";
const TRANSFORMERS_URL = "https://cdn.jsdelivr.net/npm/@huggingface/transformers@3.5.1";
const GEMMA_F16 = "gemma3-1b-it-q4f16_1-MLC";   // about 570 MB
const SMALL_F32 = "Qwen2.5-0.5B-Instruct-q4f32_1-MLC";   // for graphics chips without 16-bit support (Gemma 3 needs 16-bit)
const BACKUP_MODEL = "HuggingFaceTB/SmolLM2-360M-Instruct";   // about 370 MB

let engine = null;     // the loaded engine: { name, label, reply(messages, opts) }

// Which engine should this device use?
export async function pickEngine() {
  const asked = new URLSearchParams(location.search).get("engine");
  if (asked === "mock") return { kind: "mock", label: "Test mode (no AI, pretend replies)" };
  if (asked === "backup") return { kind: "backup", label: "Backup AI (SmolLM2 360M, on the processor)" };
  try {
    const adapter = navigator.gpu && (await navigator.gpu.requestAdapter());
    if (adapter) {
      const f16 = adapter.features.has("shader-f16");
      return f16
        ? { kind: "webllm", model: GEMMA_F16, label: "Gemma 3 1B on the graphics chip" }
        : { kind: "webllm", model: SMALL_F32, label: "Qwen2.5 0.5B on the graphics chip (this chip can't run Gemma: no 16-bit support)" };
    }
  } catch (e) { /* no WebGPU: fall through to the backup */ }
  return { kind: "backup", label: "Backup AI (SmolLM2 360M, on the processor). No WebGPU on this device." };
}

// Download (first time) and start the AI. onProgress(fraction 0-1, text).
export async function startAI(choice, onProgress) {
  if (choice.kind === "mock") { engine = mockEngine(); onProgress(1, "Test mode is ready."); return engine; }
  if (choice.kind === "webllm") {
    const webllm = await import(WEBLLM_URL);
    const llm = await webllm.CreateMLCEngine(choice.model, {
      initProgressCallback: (r) => onProgress(r.progress, r.text),
    });
    engine = {
      name: "webllm", label: choice.label,
      async reply(messages, { temperature, maxTokens, onToken }) {
        // Gemma has no separate "system" role, so the bot's job goes at the top of the first message.
        const stream = await llm.chat.completions.create({
          messages: choice.model === GEMMA_F16 ? foldSystem(messages) : messages, temperature, max_tokens: maxTokens, stream: true,
        });
        let text = "";
        for await (const chunk of stream) {
          const piece = chunk.choices[0]?.delta?.content || "";
          if (piece) { text += piece; onToken?.(text); }
        }
        return text.trim();
      },
    };
    return engine;
  }
  // Backup: Transformers.js on the processor (WebAssembly).
  const tf = await import(TRANSFORMERS_URL);
  tf.env.backends.onnx.wasm.proxy = true;   // run the AI in a background worker so the page doesn't freeze
  const files = {};
  const gen = await tf.pipeline("text-generation", BACKUP_MODEL, {
    dtype: "q8", device: "wasm",
    progress_callback: (p) => {
      if (p.status !== "progress" || !p.total) return;
      files[p.file] = [p.loaded, p.total];
      const all = Object.values(files), got = all.reduce((s, f) => s + f[0], 0), tot = all.reduce((s, f) => s + f[1], 0);
      onProgress(got / tot, `Downloading the backup AI: ${Math.round(got / 1e6)} of ${Math.round(tot / 1e6)} MB`);
    },
  });
  engine = {
    name: "backup", label: choice.label,
    async reply(messages, { temperature, maxTokens, onToken }) {
      let text = "";
      const streamer = new tf.TextStreamer(gen.tokenizer, {
        skip_prompt: true, skip_special_tokens: true,
        callback_function: (piece) => { text += piece; onToken?.(text); },
      });
      await gen(messages, { max_new_tokens: maxTokens, temperature: Math.max(temperature, 0.01),
        do_sample: temperature > 0, streamer });
      return text.trim();
    },
  };
  return engine;
}

export function currentEngine() { return engine; }

// Put the system message at the top of the first user message.
function foldSystem(messages) {
  const sys = messages.filter((m) => m.role === "system").map((m) => m.content).join("\n\n");
  const rest = messages.filter((m) => m.role !== "system").map((m) => ({ ...m }));
  const first = rest.find((m) => m.role === "user");
  if (sys && first) first.content = sys + "\n\n" + first.content;
  return rest;
}

// ---------- Test mode: pretend replies, no download ----------
function mockEngine() {
  return {
    name: "mock", label: "Test mode (no AI, pretend replies)",
    async reply(messages, { onToken, task }) {
      const last = messages[messages.length - 1].content;
      const all = messages.map((m) => m.content).join("\n");
      let text;
      if (task === "finder") {
        const ids = [...all.matchAll(/"id":\s*"([^"]+)"/g)].map((m) => m[1]).slice(0, 2);
        text = JSON.stringify({ picks: ids, reason: "Test mode picked the first two items." });
      } else if (task === "summarise") {
        text = "- (test mode) This is where the summary goes.\n- The real AI writes 3 short points.\n- Start the AI to try it.";
      } else if (task === "faq") {
        const fact = all.match(/A: (.+)/);
        text = "(test mode) " + (fact ? fact[1] : "I'd answer from your FAQ facts here.");
      } else {
        text = "(test mode) You said: \"" + last.split("\n").pop().slice(0, 80) + "\". The real AI would reply here.";
      }
      let shown = "";
      for (const word of text.split(/(?<= )/)) {
        await new Promise((r) => setTimeout(r, 30));
        shown += word; onToken?.(shown);
      }
      return text;
    },
  };
}
