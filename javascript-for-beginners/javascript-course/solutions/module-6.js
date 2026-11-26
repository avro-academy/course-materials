// Module 6: Objects and data (solutions)

// ─── Task 1 ─────────────────────────────────────────────────────────────────
const drink = {
  name: "Iced latte",
  price: 6.5,
  size: "large",
};

console.log(drink.name);  // Iced latte
console.log(drink.price); // 6.5

drink.price = 6.8;
drink.isVegan = true;
console.log(drink); // { name: 'Iced latte', price: 6.8, size: 'large', isVegan: true }

// ─── Task 2 ─────────────────────────────────────────────────────────────────
const shift = {
  name: "Jordan",
  hours: 6,
  rate: 25,
  pay() {
    return this.hours * this.rate;
  },
};

console.log(`${shift.name} earns $${shift.pay()} for this shift`); // Jordan earns $150 for this shift

// ─── Task 3 ─────────────────────────────────────────────────────────────────
const roster = [
  { name: "Mel", day: "Monday", hours: 6 },
  { name: "Sam", day: "Saturday", hours: 5 },
  { name: "Ali", day: "Saturday", hours: 4 },
  { name: "Priya", day: "Sunday", hours: 7 },
  { name: "Jordan", day: "Tuesday", hours: 3 },
];

// a)
const saturday = roster.filter((s) => s.day === "Saturday").map((s) => s.name);
console.log(saturday); // [ 'Sam', 'Ali' ]

// b)
const jordan = roster.find((s) => s.name === "Jordan");
console.log(`${jordan.name} works ${jordan.hours} hours on ${jordan.day}`);

// c)
let totalHours = 0;
for (const s of roster) {
  totalHours += s.hours;
}
console.log(`Total: ${totalHours} hours`); // Total: 25 hours

// d)
const longShifts = roster.filter((s) => s.hours > 5).map((s) => s.name);
console.log(longShifts); // [ 'Mel', 'Priya' ]

// ─── Task 4 ─────────────────────────────────────────────────────────────────
const rosterJson = JSON.stringify(roster);
console.log(rosterJson);
console.log(typeof rosterJson); // string

const productsJson = '[{"name":"Muffin","price":4},{"name":"Wrap","price":9.5}]';
const products = JSON.parse(productsJson);
console.log(products[0].name); // Muffin
