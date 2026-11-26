// To-do list that remembers (finished version)

const form = document.querySelector("#todo-form");
const input = document.querySelector("#task-input");
const list = document.querySelector("#task-list");
const summary = document.querySelector("#summary");

// Step 5: load saved tasks, or start with an empty array.
// Each task is an object: { text: "Wipe tables", done: false }
let tasks = JSON.parse(localStorage.getItem("tasks")) || [];

function save() {
  localStorage.setItem("tasks", JSON.stringify(tasks));
}

// Draw the whole list on the page from the tasks array
function render() {
  list.innerHTML = ""; // clear the list (safe: it's an empty string)

  for (const task of tasks) {
    const item = document.createElement("li");
    if (task.done) item.classList.add("done");

    const checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.checked = task.done;
    checkbox.setAttribute("aria-label", `Done: ${task.text}`);
    checkbox.addEventListener("change", () => {
      task.done = checkbox.checked;
      save();
      render();
    });

    const text = document.createElement("span");
    text.textContent = task.text; // textContent keeps user text safe

    const remove = document.createElement("button");
    remove.textContent = "Delete";
    remove.addEventListener("click", () => {
      tasks = tasks.filter((t) => t !== task);
      save();
      render();
    });

    item.append(checkbox, text, remove);
    list.append(item);
  }

  // Summary: "2 of 3 tasks left"
  const left = tasks.filter((t) => !t.done).length;
  if (tasks.length === 0) {
    summary.textContent = "No tasks yet. Add one above!";
  } else {
    summary.textContent = `${left} of ${tasks.length} ${tasks.length === 1 ? "task" : "tasks"} left`;
  }
}

// Add a task when the form is submitted (Add button or Enter)
form.addEventListener("submit", (event) => {
  event.preventDefault();
  const text = input.value.trim();
  if (text === "") return; // ignore empty tasks
  tasks.push({ text: text, done: false });
  input.value = "";
  save();
  render();
});

render();
