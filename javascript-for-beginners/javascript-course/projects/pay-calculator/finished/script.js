// Shift pay calculator (finished version)
// Example rates for practice only. Real pay rates depend on your award.

// Steps 1 and 2: the functions from Module 5
const BASE_RATE = 25;

function getMultiplier(day) {
  if (day === "Saturday") return 1.25;
  if (day === "Sunday") return 1.5;
  return 1;
}

function shiftPay(hours, day) {
  return hours * BASE_RATE * getMultiplier(day);
}

// Step 3: select the elements
const hoursInput = document.querySelector("#hours");
const daySelect = document.querySelector("#day");
const button = document.querySelector("#calculate");
const result = document.querySelector("#result");

// Step 4: respond to the click
button.addEventListener("click", () => {
  const hours = Number(hoursInput.value);
  const day = daySelect.value;
  result.hidden = false;

  // Validation: check what the user typed before using it
  if (hoursInput.value === "" || hours <= 0) {
    result.textContent = "Please enter the number of hours you worked.";
    result.classList.add("error");
    return;
  }

  const pay = shiftPay(hours, day);
  result.classList.remove("error");
  result.textContent = `${hours} hours on ${day} = $${pay.toFixed(2)}`;
});
