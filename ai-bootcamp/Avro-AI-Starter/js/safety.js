// js/safety.js: checks in code, before the AI sees anything.
// Rules in the prompt work most of the time; these work every time.
// Change the settings in SAFETY in js/config.js.
import { SAFETY } from "./config.js";

// Returns { ok: true } or { ok: false, reply: "what to show instead" }.
export function checkMessage(text) {
  const clean = text.trim();
  if (!clean) return { ok: false, reply: "" };
  if (clean.length > SAFETY.maxLength) return { ok: false, reply: SAFETY.tooLongReply };
  const lower = clean.toLowerCase();
  const hit = SAFETY.blockedWords.find((w) => w && lower.includes(w.toLowerCase()));
  if (hit) return { ok: false, reply: SAFETY.blockedReply };
  return { ok: true };
}
