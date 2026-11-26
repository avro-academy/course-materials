// Café Helper 2.0 in the browser. The conversation is kept on the server (by the checkpointer):
// the page only sends the new message, and shows what the server sends back.
const chat = document.querySelector("#chat");
const form = document.querySelector("#ask");
const input = document.querySelector("#message");
const button = form.querySelector("button");
const greeting = chat.innerHTML;
let polling = null;

function addMessage(kind, text, tools) {
  const div = document.createElement("div");
  div.className = "msg " + kind;
  div.textContent = text;
  if (tools && tools.length) {
    const small = document.createElement("small");
    small.className = "tools";
    small.textContent = "🔧 " + tools.join(", ");
    div.append(small);
  }
  chat.append(div);
  chat.scrollTop = chat.scrollHeight;
  return div;
}

function show(data) {
  chat.innerHTML = greeting;
  data.messages.forEach((m, i) => {
    const last = i === data.messages.length - 1;
    addMessage(m.role === "user" ? "user" : (data.waiting && last ? "bot waiting" : "bot"), m.text, m.tools);
  });
  // While a booking waits for staff, ask the server for news every 4 seconds
  button.disabled = data.waiting;
  if (data.waiting && !polling) polling = setInterval(refresh, 4000);
  if (!data.waiting && polling) { clearInterval(polling); polling = null; }
}

async function refresh() {
  const res = await fetch("/api/chat");
  if (res.ok) show(await res.json());
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const text = input.value.trim();
  if (!text) return;
  input.value = "";
  button.disabled = true;
  addMessage("user", text);
  const thinking = addMessage("bot", "Thinking…");
  try {
    const res = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text }),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || "Something went wrong.");
    show(data);
  } catch (err) {
    thinking.textContent = err.message;
    thinking.classList.add("error");
    button.disabled = false;
  }
  if (!button.disabled) input.focus();
});

refresh();
