// Module 5: Functions (solutions)

// ─── Task 1 ─────────────────────────────────────────────────────────────────
function sayHello(name) {
  return `Hello, ${name}!`;
}
console.log(sayHello("Priya")); // Hello, Priya!
console.log(sayHello("Sam"));   // Hello, Sam!

function minutesToHours(minutes) {
  return minutes / 60;
}
console.log(minutesToHours(90)); // 1.5
console.log(minutesToHours(45)); // 0.75

// ─── Task 2 ─────────────────────────────────────────────────────────────────
function addGst(price) {
  return price * 1.1;
}

function formatPrice(amount) {
  return `$${amount.toFixed(2)}`;
}

console.log(formatPrice(addGst(5))); // $5.50

// ─── Task 3 ─────────────────────────────────────────────────────────────────
const minutesToHoursArrow = (minutes) => minutes / 60;
console.log(minutesToHoursArrow(90)); // 1.5

const isWeekday = (day) => day !== "Saturday" && day !== "Sunday";
console.log(isWeekday("Tuesday"));  // true
console.log(isWeekday("Saturday")); // false

function makeCoffee(type = "flat white") {
  return `One ${type} coming up!`;
}
console.log(makeCoffee("chai latte")); // One chai latte coming up!
console.log(makeCoffee());             // One flat white coming up!

// ─── Task 4 ─────────────────────────────────────────────────────────────────
const BASE_RATE = 25;

function getMultiplier(day) {
  if (day === "Public holiday") return 2.5; // challenge
  if (day === "Saturday") return 1.25;
  if (day === "Sunday") return 1.5;
  return 1;
}

function shiftPay(hours, day) {
  return hours * BASE_RATE * getMultiplier(day);
}

const week = [
  { day: "Monday", hours: 5 },
  { day: "Wednesday", hours: 4 },
  { day: "Saturday", hours: 6 },
  { day: "Sunday", hours: 4.5 },
  { day: "Public holiday", hours: 4 }, // challenge
];

let total = 0;
for (const shift of week) {
  const pay = shiftPay(shift.hours, shift.day);
  console.log(`${shift.day}: $${pay.toFixed(2)}`);
  total += pay;
}
console.log(`Week total: $${total.toFixed(2)}`);

// Monday: $125.00
// Wednesday: $100.00
// Saturday: $187.50
// Sunday: $168.75
// Public holiday: $250.00
// Week total: $831.25
