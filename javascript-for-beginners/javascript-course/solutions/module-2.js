// Module 2: Values and variables (solutions)
// There's often more than one right answer. If yours prints the same thing, it's fine!

// ─── Task 1 ─────────────────────────────────────────────────────────────────
const cafeName = "Corner Café";
let coffeesSold = 0;

coffeesSold++;
coffeesSold += 1;
coffeesSold = coffeesSold + 1;

console.log(cafeName);    // Corner Café
console.log(coffeesSold); // 3

// ─── Task 2 ─────────────────────────────────────────────────────────────────
const RATE = 25;
const totalHours = 4 + 5.5 + 6;
console.log(totalHours); // 15.5

const weeklyPay = totalHours * RATE;
console.log(weeklyPay); // 387.5

const muffinWithGst = 4.95 * 1.1;
console.log(muffinWithGst.toFixed(2)); // 5.45

// ─── Task 3 ─────────────────────────────────────────────────────────────────
const typedName = "   alex nguyen   ";
const cleanName = typedName.trim();

console.log(cleanName.length);        // 11
console.log(cleanName.toUpperCase()); // ALEX NGUYEN

const lattes = 2;
console.log(`Order for ${cleanName}: ${lattes} lattes`); // Order for alex nguyen: 2 lattes

// ─── Task 4 ─────────────────────────────────────────────────────────────────
const hoursFromForm = "7.5";
const ageFromForm = "17";

// a) "7.5" is a string, so + joins the text instead of adding.
console.log(hoursFromForm + 2); // 7.52

// b)
const hours = Number(hoursFromForm);
console.log(hours + 2); // 9.5

// c)
const age = Number(ageFromForm);
console.log(age >= 18); // false

// d)
console.log(typeof hoursFromForm); // string
console.log(typeof hours);         // number
