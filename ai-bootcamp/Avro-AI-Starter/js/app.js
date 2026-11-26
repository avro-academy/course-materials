// js/app.js: connects the page to the AI. You'll change this in later weeks.
import { APP, BOT, FEATURES, AI } from "./config.js";
import { pickEngine, startAI, currentEngine } from "./ai.js";
import { chatMessages, faqMessages, finderMessages, summariseMessages, promptAsText } from "./prompt.js";
import { checkMessage } from "./safety.js";

const $ = (s) => document.querySelector(s);
let creativity = AI.creativity;
let showPrompt = false;
const history = [];              // the chat so far: { role, content }
let faq = [], products = [];

// ---------- Your app's name, colour and tabs ----------
document.title = APP.name;
$("#app-name").textContent = APP.name;
$("#app-tagline").textContent = APP.tagline;
document.querySelector('meta[name="theme-color"]').content = APP.colour;
for (const [tab, on] of Object.entries(FEATURES)) {
  if (!on) { document.querySelector(`[data-tab="${tab}"]`).hidden = true; }
}
$("#tabs").addEventListener("click", (e) => {
  const tab = e.target.dataset.tab; if (!tab) return;
  document.querySelectorAll("#tabs button").forEach((b) => b.classList.toggle("is-on", b === e.target));
  document.querySelectorAll(".panel").forEach((p) => p.classList.toggle("is-on", p.id === "tab-" + tab));
});

// ---------- Data ----------
async function loadData() {
  try { faq = await (await fetch("data/faq.json")).json(); } catch (e) { console.error("Couldn't read data/faq.json. Check its commas and quotes.", e); }
  try { products = await (await fetch("data/products.json")).json(); } catch (e) { console.error("Couldn't read data/products.json. Check its commas and quotes.", e); }
}

// ---------- Starting the AI ----------
let choice;
async function setup() {
  if (location.protocol === "file:") {
    $("#engine-label").textContent = "This page needs a web server. In VS Code, right-click index.html → Open with Live Server.";
    return;
  }
  await loadData();
  choice = await pickEngine();
  $("#engine-label").textContent = "This device will use: " + choice.label;
  $("#start-btn").disabled = false;
  addMsg("#chat-log", "bot", BOT.greeting);
  if (choice.kind === "mock") $("#start-btn").click();
}
$("#start-btn").addEventListener("click", async () => {
  $("#start-btn").disabled = true;
  $(".bar").hidden = false;
  try {
    await startAI(choice, (fraction, text) => {
      $(".bar i").style.width = Math.round(fraction * 100) + "%";
      $("#start-text").textContent = text;
    });
    $("#start").hidden = true;
    $("#engine-info").textContent = "AI: " + currentEngine().label;
  } catch (e) {
    console.error(e);
    $("#start-text").textContent = "AI isn't available on this device: " + (e.message || e) + " Update Chrome or Edge and try again.";
    $("#start-btn").disabled = false;
  }
});

// ---------- Helpers ----------
function addMsg(log, who, text) {
  const div = document.createElement("div");
  div.className = "msg " + who; div.textContent = text;
  $(log).append(div); div.scrollIntoView({ block: "end" });
  return div;
}
function ready(log) {
  if (currentEngine()) return true;
  addMsg(log, "note", "Click Start the AI first.");
  return false;
}
function show(messages) {
  $("#prompt-view").hidden = !showPrompt;
  if (showPrompt) $("#prompt-view").textContent = "What the AI received:\n\n" + promptAsText(messages);
}
async function ask(messages, task, onToken) {
  show(messages);
  return currentEngine().reply(messages, { temperature: creativity, maxTokens: AI.maxReplyTokens, onToken, task });
}

// ---------- Chat ----------
$("#chat-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const text = $("#chat-input").value.trim(); if (!text) return;
  if (!ready("#chat-log")) return;
  $("#chat-input").value = "";
  addMsg("#chat-log", "user", text);
  const check = checkMessage(text);
  if (!check.ok) { addMsg("#chat-log", "bot", check.reply); return; }
  const bubble = addMsg("#chat-log", "bot", "…");
  const reply = await ask(chatMessages(history, text, AI.historyTurns), "chat", (t) => { bubble.textContent = t; });
  bubble.textContent = reply;
  history.push({ role: "user", content: text }, { role: "assistant", content: reply });
});

// ---------- FAQ bot ----------
// Finds the facts that share the most words with the question.
// Common words like "you" and "what" don't count.
const SKIP = new Set("the and are you your can what when where which who how does have has for with any there this that our from".split(" "));
function findFacts(question, max = 3) {
  const words = (s) => new Set((s.toLowerCase().match(/[a-z0-9]{3,}/g) || []).filter((w) => !SKIP.has(w)));
  const q = words(question);
  return faq
    .map((f) => ({ f, score: [...words(f.q + " " + f.a)].filter((w) => q.has(w)).length }))
    .filter((x) => x.score > 0)
    .sort((a, b) => b.score - a.score)
    .slice(0, max)
    .map((x) => x.f);
}
$("#faq-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const text = $("#faq-input").value.trim(); if (!text) return;
  if (!ready("#faq-log")) return;
  $("#faq-input").value = "";
  addMsg("#faq-log", "user", text);
  const check = checkMessage(text);
  if (!check.ok) { addMsg("#faq-log", "bot", check.reply); return; }
  const facts = findFacts(text);
  if (!facts.length) { addMsg("#faq-log", "bot", BOT.unknownReply); return; }
  const bubble = addMsg("#faq-log", "bot", "…");
  bubble.textContent = await ask(faqMessages(facts, text), "faq", (t) => { bubble.textContent = t; });
});

// ---------- Finder ----------
// The AI must reply in JSON. We check it: only ids that really exist are shown.
function readPicks(reply) {
  const json = reply.match(/\{[\s\S]*\}/);
  if (!json) return null;
  try {
    const data = JSON.parse(json[0]);
    const picks = (data.picks || []).map((id) => products.find((p) => p.id === id)).filter(Boolean);
    return { picks, reason: String(data.reason || "") };
  } catch (e) { return null; }
}
// Backup when the AI's reply isn't valid JSON: pick items that share words with the request.
function wordMatch(wish) {
  const words = (s) => (s.toLowerCase().match(/[a-z0-9]{3,}/g) || []).filter((w) => !SKIP.has(w));
  const want = new Set(words(wish));
  const picks = products
    .map((p) => ({ p, score: words(p.name + " " + p.tags.join(" ") + " " + p.about).filter((w) => want.has(w)).length }))
    .filter((x) => x.score > 0).sort((a, b) => b.score - a.score).slice(0, 3).map((x) => x.p);
  return { picks, reason: picks.length ? "These match the words you used." : "" };
}
$("#finder-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const text = $("#finder-input").value.trim(); if (!text) return;
  if (!currentEngine()) { $("#finder-reason").textContent = "Click Start the AI first."; return; }
  const check = checkMessage(text);
  if (!check.ok) { $("#finder-reason").textContent = check.reply; return; }
  $("#finder-reason").textContent = "Thinking…"; $("#finder-results").innerHTML = "";
  const reply = await ask(finderMessages(products, text), "finder");
  console.log("Finder: the AI replied", reply);   // F12 > Console shows exactly what came back
  let result = readPicks(reply);
  if (!result || !result.picks.length) result = wordMatch(text);
  if (!result || !result.picks.length) { $("#finder-reason").textContent = "Sorry, I couldn't find a match. Try describing it another way."; return; }
  $("#finder-reason").textContent = result.reason;
  for (const p of result.picks) {
    const card = document.createElement("div"); card.className = "item";
    card.innerHTML = `<b></b><span class="price"></span><p class="small"></p>`;
    card.querySelector("b").textContent = p.name;
    card.querySelector(".price").textContent = "$" + p.price.toFixed(2);
    card.querySelector("p").textContent = p.about;
    for (const t of p.tags) { const s = document.createElement("span"); s.className = "tag"; s.textContent = t; card.append(s); }
    $("#finder-results").append(card);
  }
});

// ---------- Summariser ----------
$("#sum-btn").addEventListener("click", async () => {
  const text = $("#sum-input").value.trim(); if (!text) return;
  if (!currentEngine()) { $("#sum-out").textContent = "Click Start the AI first."; return; }
  if (text.length > 6000) { $("#sum-out").textContent = "That's too long for this small AI. Try under 6,000 characters."; return; }
  $("#sum-out").textContent = "…";
  $("#sum-out").textContent = await ask(summariseMessages(text), "summarise", (t) => { $("#sum-out").textContent = t; });
});

// ---------- Settings ----------
$("#temp").value = creativity; $("#temp-out").textContent = creativity;
$("#temp").addEventListener("input", (e) => { creativity = +e.target.value; $("#temp-out").textContent = creativity; });
$("#show-prompt").addEventListener("change", (e) => { showPrompt = e.target.checked; if (!showPrompt) $("#prompt-view").hidden = true; });
$("#clear-chat").addEventListener("click", () => {
  history.length = 0; $("#chat-log").innerHTML = ""; addMsg("#chat-log", "bot", BOT.greeting);
});

setup();
