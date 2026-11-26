# Module 6: Dictionaries and data — solutions

# ── Task 1: A product dictionary ──────────────────────────────

product = {"name": "Blueberry muffin", "price": 4.75, "in_stock": True}
print(f"{product['name']} costs ${product['price']:.2f}")
product["price"] = 5
product["category"] = "Food"
print(product)

# ── Task 2: Safe lookups and looping ──────────────────────────

staff = {"name": "Jordan", "role": "Barista"}
prices = {"Flat white": 4.5, "Latte": 5, "Chai": 5.5}

print(staff.get("phone", "No phone saved"))
for item, price in prices.items():
    print(f"{item}: ${price:.2f}")

# ── Task 3: The roster: a list of dictionaries ────────────────

roster = [
    {"name": "Mel", "day": "Monday", "hours": 6},
    {"name": "Sam", "day": "Saturday", "hours": 5},
    {"name": "Ali", "day": "Saturday", "hours": 4},
    {"name": "Priya", "day": "Sunday", "hours": 7},
]

print([s["name"] for s in roster if s["day"] == "Saturday"])
print("Total hours:", sum(s["hours"] for s in roster))
longest = max(roster, key=lambda s: s["hours"])
print(f"Longest shift: {longest['name']} ({longest['hours']} h)")
print([s["name"] for s in roster if s["hours"] > 5])

# ── Task 4: Count the orders ──────────────────────────────────

orders = ["Latte", "Flat white", "Latte", "Chai", "Latte", "Flat white"]
counts = {}
for drink in orders:
    counts[drink] = counts.get(drink, 0) + 1
print(counts)
print("Most popular:", max(counts, key=counts.get))
