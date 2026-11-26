// Take a shift without reloading the page, using the JSON API.
// Without JavaScript, the form still works the normal way.
const list = document.querySelector("#shifts");
const statusBox = document.querySelector("#status");

if (list) {
  list.addEventListener("submit", async (event) => {
    const form = event.target.closest("form.claim");
    if (!form) return;
    event.preventDefault();
    const button = form.querySelector("button");
    button.disabled = true;

    const response = await fetch(`/api/shifts/${form.dataset.id}/claim`, {
      method: "POST",
      headers: { "X-CSRF-Token": list.dataset.csrf },
    });
    const data = await response.json();

    statusBox.hidden = false;
    if (response.ok) {
      statusBox.textContent = data.message;
      form.closest("li").remove();
      if (!list.querySelector("li")) {
        list.outerHTML = '<p class="empty">No open shifts right now. 🎉</p>';
      }
    } else {
      statusBox.textContent = data.error;
      button.disabled = false;
    }
  });
}
