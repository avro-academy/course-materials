# Module 7: Files, errors and modules — exercises
# Write your code under each task, then run this file: python module7_exercises.py

# ── Task 1: Save and read a CSV ───────────────────────────────
# Write `roster` to `roster.csv` with `csv.DictWriter`, then read it back with `csv.DictReader`
# and print each person's pay at $25 an hour. (Remember: everything read from a CSV is text.)

import csv

roster = [
    {"name": "Mel", "day": "Monday", "hours": 6},
    {"name": "Sam", "day": "Saturday", "hours": 5},
]


# ── Task 2: Don't crash ───────────────────────────────────────
# Write `ask_number(question)` that keeps asking until the user types a number greater than 0,
# using `try` / `except ValueError`. Use it to ask for hours and rate, then print the pay.

def ask_number(question):
    pass



# ── Task 3: Using modules ─────────────────────────────────────
# 1. Use `random.choice` to pick today's special from a list.
# 2. Use `math.ceil` to work out how many 12-packs of milk you need for 50 litres.
# 3. Use `datetime.date.today()` to work out how many days until your birthday.

import random
import math
from datetime import date

specials = ["Banana bread", "Avocado toast", "Toastie"]

