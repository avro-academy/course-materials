const form = document.getElementById("ask");
const input = document.getElementById("question");
const result = document.getElementById("result");
const answerText = document.getElementById("answer");
const sourcesBox = document.getElementById("sources");
const button = form.querySelector("button");

async function ask(question) {
  result.hidden = false;
  answerText.textContent = "Looking through the documents…";
  answerText.className = "waiting";
  sourcesBox.replaceChildren();
  button.disabled = true;
  try {
    const response = await fetch("/api/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question }),
    });
    const data = await response.json().catch(() => ({}));
    if (!response.ok) {
      answerText.textContent = data.error || "Something went wrong. Please try again.";
      answerText.className = "error";
      return;
    }
    answerText.textContent = data.answer;
    answerText.className = "";
    for (const source of data.sources) {
      const box = document.createElement("div");
      box.className = "source";
      const link = document.createElement("a");
      link.href = source.link;
      link.target = "_blank";
      link.rel = "noopener";
      link.textContent = `[${source.n}] ${source.label}`;
      const excerpt = document.createElement("p");
      excerpt.textContent = source.excerpt;
      box.append(link, excerpt);
      sourcesBox.append(box);
    }
  } catch {
    answerText.textContent = "Couldn't reach the assistant. Is the app running?";
    answerText.className = "error";
  } finally {
    button.disabled = false;
  }
}

form.addEventListener("submit", (event) => {
  event.preventDefault();
  const question = input.value.trim();
  if (question) ask(question);
});

for (const example of document.querySelectorAll(".example")) {
  example.addEventListener("click", () => {
    input.value = example.textContent;
    ask(example.textContent);
  });
}
