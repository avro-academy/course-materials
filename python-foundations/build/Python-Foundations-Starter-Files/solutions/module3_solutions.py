# Module 3: Making decisions — solutions

# ── Task 1: Open or closed? ───────────────────────────────────

hour = 9

if hour >= 7 and hour < 15:
    print("Open")
else:
    print("Closed")

# ── Task 2: Stock levels ──────────────────────────────────────

stock = 12

if stock == 0:
    print("Out of stock")
elif stock < 5:
    print("Low stock — reorder soon")
elif stock < 20:
    print("In stock")
else:
    print("Plenty in stock")

hour = 14
if hour < 12:
    print("Good morning")
elif hour < 18:
    print("Good afternoon")
else:
    print("Good evening")

# ── Task 3: Free delivery ─────────────────────────────────────

total = 35
is_member = True
is_public_holiday = False

if (total >= 40 or is_member) and not is_public_holiday:
    print("Free delivery")
else:
    print("Delivery costs $6.50")
