// Module 3: Making decisions (solutions)

// ─── Task 1 ─────────────────────────────────────────────────────────────────
const temperature = 31;

if (temperature >= 30) {
  console.log("Hot day: put the cold drinks out front");
} else {
  console.log("Normal day");
}

// ─── Task 2 ─────────────────────────────────────────────────────────────────
const total = 42;
let discount = 0;

if (total < 20) {
  console.log("No discount");
} else if (total < 50) {
  console.log("5% off");
  discount = 0.05;
} else {
  console.log("10% off");
  discount = 0.1;
}

// Bonus
const afterDiscount = total * (1 - discount);
console.log(`You pay $${afterDiscount.toFixed(2)}`); // You pay $39.90

// ─── Task 3 ─────────────────────────────────────────────────────────────────
const age = 17;
const hasParentConsent = true;
const isMember = false;
const orderTotal = 35;

// a)
const canSignUp = age >= 18 || (age < 18 && hasParentConsent);
console.log(canSignUp); // true

// b)
const deliveryMessage = orderTotal > 50 || isMember ? "Free delivery" : "Delivery: $5";
console.log(deliveryMessage); // Delivery: $5

// c)
console.log(!isMember); // true
