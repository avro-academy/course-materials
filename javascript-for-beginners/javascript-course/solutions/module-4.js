// Module 4: Arrays and loops (solutions)

// ─── Task 1 ─────────────────────────────────────────────────────────────────
const menu = ["Toastie", "Muffin", "Wrap"];

console.log(menu[0]);               // Toastie
console.log(menu[menu.length - 1]); // Wrap

menu.push("Banana bread");
console.log(menu); // [ 'Toastie', 'Muffin', 'Wrap', 'Banana bread' ]

menu[1] = "Blueberry muffin";
console.log(menu); // [ 'Toastie', 'Blueberry muffin', 'Wrap', 'Banana bread' ]

console.log(menu.includes("Wrap")); // true

// ─── Task 2 ─────────────────────────────────────────────────────────────────
const dailySales = [320.5, 410, 289.75, 502, 615.25];

for (const sales of dailySales) {
  console.log(`Sales: $${sales}`);
}

let total = 0;
for (const sales of dailySales) {
  total += sales;
}
console.log(`Total: $${total}`); // Total: $2137.5

const average = total / dailySales.length;
console.log(`Average: $${average.toFixed(2)}`); // Average: $427.50

// ─── Task 3 ─────────────────────────────────────────────────────────────────
for (let i = 1; i <= 6; i++) {
  console.log(`Table ${i}`);
}

let muffins = 5;
while (muffins > 0) {
  muffins--;
  console.log(`Sold a muffin. ${muffins} left.`);
}

// ─── Task 4 ─────────────────────────────────────────────────────────────────
const prices = [3.5, 12, 4.8, 9.95, 15, 2.2];
const staffNames = ["Mel", "Sam", "Jordan", "Priya", "Ali"];

const underFive = prices.filter((price) => price < 5);
console.log(underFive); // [ 3.5, 4.8, 2.2 ]

const plusOne = prices.map((price) => price + 1);
console.log(plusOne); // [ 4.5, 13, 5.8, 10.95, 16, 3.2 ]

const longName = staffNames.find((name) => name.length > 4);
console.log(longName); // Jordan

const sorted = [...prices].sort((a, b) => a - b);
console.log(sorted); // [ 2.2, 3.5, 4.8, 9.95, 12, 15 ]
