# Module 6: Dictionaries and data — exercises
# Write your code under each task, then run this file: python module6_exercises.py

# ── Task 1: A product dictionary ──────────────────────────────
# Make a dictionary for a product with `name`, `price` and `in_stock`.
# Print a sentence using its values, change the price, add a `category` key, and print the dictionary.

product = {}


# ── Task 2: Safe lookups and looping ──────────────────────────
# 1. Print the phone number from `staff` using `.get()` with a default of `"No phone saved"`.
# 2. Loop through `prices` with `.items()` and print each line like `Latte: $5.00`.

staff = {"name": "Jordan", "role": "Barista"}
prices = {"Flat white": 4.5, "Latte": 5, "Chai": 5.5}


# ── Task 3: The roster: a list of dictionaries ────────────────
# Using `roster`:
# 1. Print the names of everyone working on Saturday.
# 2. Print the total hours.
# 3. Print who has the longest shift.
# 4. Print everyone working more than 5 hours.

roster = [
    {"name": "Mel", "day": "Monday", "hours": 6},
    {"name": "Sam", "day": "Saturday", "hours": 5},
    {"name": "Ali", "day": "Saturday", "hours": 4},
    {"name": "Priya", "day": "Sunday", "hours": 7},
]


# ── Task 4: Count the orders ──────────────────────────────────
# Count how many times each drink was ordered and print the dictionary.
# Then print the most popular drink.

orders = ["Latte", "Flat white", "Latte", "Chai", "Latte", "Flat white"]
counts = {}

