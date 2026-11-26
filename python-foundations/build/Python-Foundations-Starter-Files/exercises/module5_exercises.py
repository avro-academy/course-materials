# Module 5: Functions — exercises
# Write your code under each task, then run this file: python module5_exercises.py

# ── Task 1: A greeting function ───────────────────────────────
# Write a function `greet(name)` that RETURNS `"Hi, <name>! Welcome to Corner Café."`.
# Call it for two people and print the results.

def greet(name):
    pass   # replace pass with your code


print(greet("Priya"))
print(greet("Sam"))

# ── Task 2: GST function ──────────────────────────────────────
# Write `add_gst(price)` that returns the price with 10% GST, rounded to 2 decimals.
# Use it to work out the total of a $20 item and a $5 item. Add a docstring.

def add_gst(price):
    pass


# Remove the # from the next two lines when your function is ready
# total = add_gst(20) + add_gst(5)
# print(total)   # should be 27.5

# ── Task 3: Default values ────────────────────────────────────
# Write `coffee_order(drink="Flat white", size="Regular", milk="Full cream")` that returns
# a sentence like `Regular Flat white with Full cream milk`. Call it with no arguments, with one,
# and with named arguments in a different order.

def coffee_order():
    pass



# ── Task 4: Shift pay calculator ──────────────────────────────
# Write `get_multiplier(day)` (Saturday 1.25, Sunday 1.5, other days 1) and `shift_pay(hours, day)`
# (hours × $25 × multiplier). Print each shift in `week` and the week's total.
# Challenge: add public holidays at 2.5 times. (Example rates only — real rates depend on your award.)

BASE_RATE = 25

def get_multiplier(day):
    pass

def shift_pay(hours, day):
    pass

week = [("Thursday", 4), ("Saturday", 6), ("Sunday", 5)]

