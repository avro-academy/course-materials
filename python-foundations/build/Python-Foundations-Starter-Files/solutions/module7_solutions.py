# Module 7: Files, errors and modules — solutions

# ── Task 1: Save and read a CSV ───────────────────────────────

import csv

roster = [
    {"name": "Mel", "day": "Monday", "hours": 6},
    {"name": "Sam", "day": "Saturday", "hours": 5},
]

with open("roster.csv", "w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=["name", "day", "hours"])
    writer.writeheader()
    writer.writerows(roster)

with open("roster.csv", newline="") as file:
    for row in csv.DictReader(file):
        print(row["name"], float(row["hours"]) * 25)

# ── Task 2: Don't crash ───────────────────────────────────────

def ask_number(question):
    while True:
        try:
            value = float(input(question))
            if value > 0:
                return value
            print("It must be more than 0.")
        except ValueError:
            print("That's not a number.")


hours = ask_number("Hours: ")
rate = ask_number("Rate: ")
print(f"Pay: ${hours * rate:.2f}")

# ── Task 3: Using modules ─────────────────────────────────────

import random
import math
from datetime import date

specials = ["Banana bread", "Avocado toast", "Toastie"]
print("Today's special:", random.choice(specials))
print("Packs of milk:", math.ceil(50 / 12))

today = date.today()
birthday = date(today.year, 8, 21)   # change to your birthday
if birthday < today:
    birthday = date(today.year + 1, 8, 21)
print("Days until my birthday:", (birthday - today).days)
