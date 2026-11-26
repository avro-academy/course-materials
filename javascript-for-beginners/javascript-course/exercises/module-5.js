// Module 5: Functions
// Do each task, then check your answer in solutions/module-5.js.

// ─── Task 1: your first functions (lesson: Functions) ───────────────────────
// a) Write a function sayHello(name) that RETURNS "Hello, <name>!".
//    Print the result for two different names.
// b) Write a function minutesToHours(minutes) that returns the hours
//    (e.g. 90 minutes → 1.5). Print minutesToHours(90) and minutesToHours(45).


// ─── Task 2: return values you can reuse (lesson: Functions) ────────────────
// a) Write a function addGst(price) that returns the price with 10% GST.
// b) Write a function formatPrice(amount) that returns a string like "$5.50"
//    (use toFixed(2)).
// c) Use both together to print the price of a $5 muffin with GST: "$5.50".


// ─── Task 3: arrow functions and defaults (lesson: Arrow functions…) ────────
// a) Rewrite minutesToHours from Task 1 as an arrow function.
// b) Write an arrow function isWeekday(day) that returns true for Monday
//    to Friday and false for Saturday and Sunday.
// c) Write a function makeCoffee(type = "flat white") that returns
//    "One <type> coming up!". Call it with and without an argument.


// ─── Task 4: shift pay calculator (lesson: Project: shift pay calculator) ───
// Example rates for practice only: $25 an hour, Saturday x1.25, Sunday x1.5.
const BASE_RATE = 25;
// a) Write getMultiplier(day) that returns 1.25 for Saturday, 1.5 for Sunday
//    and 1 for any other day.
// b) Write shiftPay(hours, day) that returns hours * BASE_RATE * the multiplier.
// c) Use a loop to print the pay for each shift in this week, and the total:
const week = [
  { day: "Monday", hours: 5 },
  { day: "Wednesday", hours: 4 },
  { day: "Saturday", hours: 6 },
  { day: "Sunday", hours: 4.5 },
];
// Challenge: add public holidays at 2.5 times the base rate ("Public holiday"),
// and add a public holiday shift to the week.
