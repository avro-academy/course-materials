# Avro AI Starter

The app you'll build on in Avro Academy's AI App Bootcamp. It has an AI chat, an FAQ bot, a product finder and a summariser, and the AI runs **inside the browser on your own device**: no API keys, no cloud bills, and nothing anyone types leaves the device.

## Run it

1. Open this folder in VS Code (File → Open Folder, the folder with `index.html` inside).
2. Right-click `index.html` → **Open with Live Server**. (Double-clicking the file won't work: the app needs a web server, and the address must start with `http://`.)
3. Add `?engine=mock` to the end of the address (for example `http://127.0.0.1:5500/?engine=mock`) to try every tab with pretend replies and no download.
4. Remove `?engine=mock`, click **Start the AI**, and ask: "What time do you open?"

The first start downloads the AI (about 570 MB), so use home or college Wi-Fi. The browser saves it, so after that it starts in seconds, even offline.

## Which AI?

| Your device | The app uses |
|---|---|
| Chrome or Edge with WebGPU and 16-bit support | Gemma 3 1B on the graphics chip (about 570 MB) |
| WebGPU without 16-bit support | Qwen2.5 0.5B on the graphics chip (Gemma 3 needs 16-bit support) |
| No WebGPU | Backup AI: SmolLM2 360M on the processor (about 370 MB, slower and less clever) |

Gemma and Qwen run with [WebLLM](https://webllm.mlc.ai); the backup uses [Transformers.js](https://huggingface.co/docs/transformers.js). Add `?engine=backup` to force the backup AI. Check a computer at https://avro.academy/device-check.

## The files

| File | What it is | When you change it |
|---|---|---|
| `js/config.js` | Your app's name, colour, the bot's job, rules and examples, which tabs show, safety settings | Session 1A, then every week |
| `css/style.css` | How it looks. Change `--brand` to your colour | Any time |
| `data/faq.json` | Facts the FAQ bot answers from: `{ "q": "...", "a": "..." }` | Week 3 |
| `data/products.json` | Items the Finder picks from: id, name, price, tags, about | Week 4 |
| `js/prompt.js` | Builds what the AI reads before every reply | Weeks 3–4 |
| `js/safety.js` | Checks in code before the AI sees a message | Week 6 |
| `js/app.js` | Connects the page to the AI | Later weeks |
| `js/ai.js` | Loads the AI. You don't need to change it | Never |
| `docs/prompt-test-log.md` | Your 6 test messages and scores | Week 2 |
| `icons/`, `manifest.webmanifest` | The app's icon and install details | Week 7 |

## The loop

Change, save, refresh (Ctrl+R), test. Tick **Settings → Show my prompt** to see exactly what the AI received.

App went blank? Press **F12 → Console**. A red error names the file and line; it's almost always a missing comma, quote or bracket in `config.js` or a JSON file.

## Put it online (GitHub Pages)

1. On GitHub, click **+ → New repository**, name it after your app (for example `netball-helper`), choose **Public**, and create it.
2. Click **uploading an existing file** and drag in everything inside this folder, keeping the `css`, `js`, `data`, `icons` and `docs` folders. Click **Commit changes**.
3. Go to **Settings → Pages**, choose branch **main** and **/ (root)**, then **Save**.
4. Wait a minute and refresh. Your link appears at the top: `https://yourname.github.io/netball-helper/`

To update it, upload the changed files the same way.

| Problem | Fix |
|---|---|
| 404 page | Wait 2 minutes. Check Pages is set to main and / (root), and `index.html` is at the top of the repository. |
| Page has no styling | The folders got flattened. Upload again, keeping the folders. |
| Works on my computer, not online | The repository must be Public. |
| Stuck at 0% | Your network may block the download. Try another Wi-Fi or a phone hotspot. |
| "AI isn't available on this device" | Update Chrome or Edge, then try again. |
| Replies are very slow | Your computer is using the backup AI. That's OK; tell your trainer. |

## Good to know

- Gemma 3 1B can hold about 4,000 tokens at once (roughly 3,000 words): the bot's job, examples, the chat so far and its reply. Keep the job and examples short.
- Small AIs guess. Give it a clear job (week 2), the facts (week 3), check what it returns (week 4) and test it (week 5).
- Gemma is made by Google and used under the [Gemma Terms of Use](https://ai.google.dev/gemma/terms). Qwen2.5 and SmolLM2 are released under the Apache 2.0 licence.

Made by Avro Academy for the AI App Bootcamp.
