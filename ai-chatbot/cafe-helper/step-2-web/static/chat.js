// Café Helper in the browser: shows the conversation and sends it to the server.
const chat = document.querySelector("#chat");
const form = document.querySelector("#ask");
const input = document.querySelector("#question");
const button = form.querySelector("button");
const messages = []; // the whole conversation, sent with every question

function addMessage(kind, text) {
  const div = document.createElement("div");
  div.className = "msg " + kind;
  div.textContent = text;
  chat.append(div);
  chat.scrollTop = chat.scrollHeight;
  return div;
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const question = input.value.trim();
  if (!question) return;
  input.value = "";
  button.disabled = true;
  addMessage("user", question);
  messages.push({ role: "user", content: question });
  const reply = addMessage("bot", "Thinking…");

  try {
    const res = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ messages }),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || "Something went wrong.");
    reply.textContent = data.reply;
    messages.push({ role: "assistant", content: data.reply });
  } catch (err) {
    reply.textContent = err.message;
    reply.classList.add("error");
    messages.pop(); // forget the question that failed
  }
  button.disabled = false;
  input.focus();
});
