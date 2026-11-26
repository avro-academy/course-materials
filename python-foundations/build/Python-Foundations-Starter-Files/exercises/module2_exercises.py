# Module 2: Values and variables — exercises
# Write your code under each task, then run this file: python module2_exercises.py

# ── Task 1: Your café in variables ────────────────────────────
# Make variables for a café: its name, how many tables it has, and the price of a coffee.
# Print each one. Then 4 more customers arrive: add 4 to a `customers` variable using `+=` and print it.

cafe_name = ""      # put your café's name in the quotes
tables = 0          # how many tables?
coffee_price = 0    # price of a coffee, e.g. 4.5
customers = 10

# print the three variables


# 4 more customers arrive: use +=



# ── Task 2: Shift maths ───────────────────────────────────────
# You worked shifts of 4, 6 and 5.5 hours at $25 an hour.
# 1. Work out the total hours and the total pay.
# 2. Print the pay as money with 2 decimal places, e.g. `$387.50`.
# 3. How many whole 8-hour days is that, and how many hours are left over? (Use `//` and `%`.)

rate = 25
shift_1 = 4
shift_2 = 6
shift_3 = 5.5

total_hours = 0   # replace 0 with a calculation
total_pay = 0     # replace 0 with a calculation

print("Total hours:", total_hours)
print(f"Total pay: ${total_pay:.2f}")

# whole 8-hour days and hours left over



# ── Task 3: Tidy a name ───────────────────────────────────────
# A customer typed their name as `"   mei   CHEN "`.
# 1. Remove the extra spaces and print it in Title Case.
# 2. Print how many characters the tidy name has.
# 3. Print an order message with an f-string: `Order for Mei Chen: 2 lattes, $9.60` (a latte is $4.80).

typed = "   mei   CHEN "
lattes = 2
latte_price = 4.8

# 1. tidy name (hint: .strip() and .title())
name = typed

# 2. number of characters


# 3. the order message



# ── Task 4: Ask and convert ───────────────────────────────────
# Ask the user for their hours worked and their hourly rate with `input()`.
# Convert both to numbers with `float()` and print their pay with 2 decimal places.
# Then print whether they worked more than 38 hours (a True/False value).

hours = input("Hours worked: ")
rate = input("Hourly rate: ")

# convert, then print the pay


# True or False: more than 38 hours?


