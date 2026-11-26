// js/prompt.js: builds exactly what the AI reads before every reply.
// Tick Settings > "Show my prompt" to see it under the chat.
import { BOT } from "./config.js";

// The bot's job + its rules, as one block of text.
export function systemText(extra = "") {
  const rules = BOT.rules.map((r, i) => `${i + 1}. ${r}`).join("\n");
  return `${BOT.job}\n\nRULES:\n${rules}${extra ? "\n\n" + extra : ""}`;
}

// The examples, as pretend earlier turns. The AI copies their style.
function exampleTurns() {
  return BOT.examples.flatMap((e) => [
    { role: "user", content: e.user },
    { role: "assistant", content: e.bot },
  ]);
}

// Chat: job + rules, examples, the conversation so far, the new message.
export function chatMessages(history, message, historyTurns) {
  return [
    { role: "system", content: systemText() },
    ...exampleTurns(),
    ...history.slice(-historyTurns),
    { role: "user", content: message },
  ];
}

// FAQ: the same job, plus the facts it may use, and nothing else.
export function faqMessages(facts, question) {
  const list = facts.length
    ? facts.map((f) => `Q: ${f.q}\nA: ${f.a}`).join("\n\n")
    : "(no facts match this question)";
  const extra = `Answer ONLY from these FACTS. If the answer isn't in them, reply exactly: "${BOT.unknownReply}"\n\nFACTS:\n${list}`;
  return [
    { role: "system", content: systemText(extra) },
    { role: "user", content: question },
  ];
}

// Finder: pick items from the list and reply in JSON only.
export function finderMessages(products, wish) {
  const list = products.map((p) => JSON.stringify({ id: p.id, name: p.name, tags: p.tags, about: p.about })).join("\n");
  return [
    { role: "system", content: `You help customers choose from this list. Reply with JSON only, no other words, in this shape:
{"picks": ["id1", "id2"], "reason": "one short sentence"}
Pick 1 to 3 ids from the list that best match what the customer wants. Only use ids from the list.
Example reply: {"picks": ["${products[0]?.id || "id1"}"], "reason": "It matches what you asked for."}

LIST:
${list}` },
    { role: "user", content: wish },
  ];
}

// Summariser.
export function summariseMessages(text) {
  return [
    { role: "system", content: "Summarise the text in exactly 3 short bullet points starting with \"- \". Use simple words. Don't add anything that isn't in the text." },
    { role: "user", content: text },
  ];
}

// Turn messages into readable text for "Show my prompt".
export function promptAsText(messages) {
  return messages.map((m) => `[${m.role}]\n${m.content}`).join("\n\n");
}
