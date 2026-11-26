// Module 6: Objects and data
// Do each task, then check your answer in solutions/module-6.js.

// ─── Task 1: objects (lesson: Objects: grouping related data) ───────────────
// a) Make an object called drink with: name "Iced latte", price 6.5, size "large".
// b) Print the name and the price, using dot notation.
// c) Change the price to 6.8, add a new property isVegan set to true,
//    then print the whole object.


// ─── Task 2: methods (lesson: Objects: grouping related data) ───────────────
// Make an object called shift with:
//   name: "Jordan", hours: 6, rate: 25
//   and a method pay() that returns hours * rate (use this.hours and this.rate).
// Print: "Jordan earns $150 for this shift" using the object and its method.


// ─── Task 3: arrays of objects (lesson: Arrays of objects) ──────────────────
const roster = [
  { name: "Mel", day: "Monday", hours: 6 },
  { name: "Sam", day: "Saturday", hours: 5 },
  { name: "Ali", day: "Saturday", hours: 4 },
  { name: "Priya", day: "Sunday", hours: 7 },
  { name: "Jordan", day: "Tuesday", hours: 3 },
];
// a) Print the names of everyone working on Saturday (filter + map).
// b) Find Jordan's shift and print "Jordan works 3 hours on Tuesday".
// c) Print the total rostered hours.
// d) Print the names of everyone working more than 5 hours.


// ─── Task 4: JSON (lesson: JSON: saving and sharing data) ───────────────────
// a) Turn the roster above into JSON text with JSON.stringify and print it.
// b) Print the typeof the JSON text.
// c) Turn this JSON text back into an array with JSON.parse,
//    and print the name of the first product:
const productsJson = '[{"name":"Muffin","price":4},{"name":"Wrap","price":9.5}]';
