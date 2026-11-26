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
    if (!res.ok) throw new Error("Something went wrong. Please try again.");

    // Read the reply piece by piece as the server sends it
    const reader = res.body.getReader();
    const decoder = new TextDecoder();
    let text = "";
    reply.textContent = "";
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      text += decoder.decode(value, { stream: true });
      reply.textContent = text;
      chat.scrollTop = chat.scrollHeight;
    }
    messages.push({ role: "assistant", content: text });
  } catch (err) {
    reply.textContent = err.message;
    reply.classList.add("error");
    messages.pop(); // forget the question that failed
  }
  button.disabled = false;
  input.focus();
});
