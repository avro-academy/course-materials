# Module 4: Lists and loops — exercises
# Write your code under each task, then run this file: python module4_exercises.py

# ── Task 1: The menu list ─────────────────────────────────────
# 1. Make a list `menu` with four food items.
# 2. Print the first item, the last item and how many items there are.
# 3. Add `"Toastie"` to the end, remove one item, and print the list sorted A–Z.

menu = []   # four items in here


# ── Task 2: Print the roster ──────────────────────────────────
# Loop through `staff` and print each name as `- Mel`.
# Then loop through `hours` and add them up to get the total.

staff = ["Mel", "Sam", "Ali", "Priya"]
hours = [6, 5, 4, 7.5]

# for loop over staff


# add up the hours with a loop
total = 0


# ── Task 3: Countdown and tickets ─────────────────────────────
# 1. Use `range` to print `Ticket 1` to `Ticket 5`.
# 2. Use a `while` loop: start with `stock = 4` and sell one at a time, printing what's left, until it's 0.
#    Then print `Sold out!`.

# 1. range


# 2. while
stock = 4


# ── Task 4: List comprehensions ───────────────────────────────
# 1. From `prices`, make a new list with 10% GST added (rounded to 2 decimals).
# 2. Make a list of only the prices under $10.
# 3. Turn `["tea", "coffee"]` into `["TEA", "COFFEE"]`.

prices = [4.5, 12, 3.2, 18, 7.5]

with_gst = []
under_10 = []

print(with_gst)
print(under_10)
