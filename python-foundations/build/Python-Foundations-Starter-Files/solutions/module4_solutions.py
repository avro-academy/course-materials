# Module 4: Lists and loops — solutions

# ── Task 1: The menu list ─────────────────────────────────────

menu = ["Banana bread", "Muffin", "Avocado toast", "Croissant"]
print(menu[0])
print(menu[-1])
print(len(menu))

menu.append("Toastie")
menu.remove("Muffin")
print(sorted(menu))

# ── Task 2: Print the roster ──────────────────────────────────

staff = ["Mel", "Sam", "Ali", "Priya"]
hours = [6, 5, 4, 7.5]

for person in staff:
    print(f"- {person}")

total = 0
for h in hours:
    total += h
print("Total hours:", total)

# ── Task 3: Countdown and tickets ─────────────────────────────

for number in range(1, 6):
    print(f"Ticket {number}")

stock = 4
while stock > 0:
    stock -= 1
    print(f"Sold one. {stock} left")
print("Sold out!")

# ── Task 4: List comprehensions ───────────────────────────────

prices = [4.5, 12, 3.2, 18, 7.5]

with_gst = [round(p * 1.1, 2) for p in prices]
under_10 = [p for p in prices if p < 10]

print(with_gst)
print(under_10)
print([d.upper() for d in ["tea", "coffee"]])
