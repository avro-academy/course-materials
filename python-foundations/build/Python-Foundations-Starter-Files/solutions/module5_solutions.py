# Module 5: Functions — solutions

# ── Task 1: A greeting function ───────────────────────────────

def greet(name):
    return f"Hi, {name}! Welcome to Corner Café."


print(greet("Priya"))
print(greet("Sam"))

# ── Task 2: GST function ──────────────────────────────────────

def add_gst(price):
    """Return the price with 10% GST added, rounded to cents."""
    return round(price * 1.1, 2)


total = add_gst(20) + add_gst(5)
print(total)

# ── Task 3: Default values ────────────────────────────────────

def coffee_order(drink="Flat white", size="Regular", milk="Full cream"):
    return f"{size} {drink} with {milk} milk"


print(coffee_order())
print(coffee_order("Latte"))
print(coffee_order(milk="Oat", drink="Chai latte", size="Large"))

# ── Task 4: Shift pay calculator ──────────────────────────────

BASE_RATE = 25

def get_multiplier(day):
    if day == "Public holiday":
        return 2.5
    if day == "Saturday":
        return 1.25
    if day == "Sunday":
        return 1.5
    return 1

def shift_pay(hours, day):
    return hours * BASE_RATE * get_multiplier(day)

week = [("Thursday", 4), ("Saturday", 6), ("Sunday", 5), ("Public holiday", 3)]
total = 0
for day, hours in week:
    pay = shift_pay(hours, day)
    print(f"{day:<14} {hours} h  ${pay:>7.2f}")
    total += pay
print(f"Week total: ${total:.2f}")
