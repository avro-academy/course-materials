"""Practice tasks for Python Foundations. Each task: (module, number, title, instructions, starter, solution)."""

MODULES = {
    2: "Values and variables",
    3: "Making decisions",
    4: "Lists and loops",
    5: "Functions",
    6: "Dictionaries and data",
    7: "Files, errors and modules",
}

TASKS = [
# ── Module 2 ─────────────────────────────────────────────
(2, 1, "Your café in variables",
"""Make variables for a café: its name, how many tables it has, and the price of a coffee.
Print each one. Then 4 more customers arrive: add 4 to a `customers` variable using `+=` and print it.""",
'''cafe_name = ""      # put your café's name in the quotes
tables = 0          # how many tables?
coffee_price = 0    # price of a coffee, e.g. 4.5
customers = 10

# print the three variables


# 4 more customers arrive: use +=


''',
'''cafe_name = "Corner Café"
tables = 8
coffee_price = 4.5
customers = 10

print(cafe_name)
print(tables)
print(coffee_price)

customers += 4
print(customers)
'''),
(2, 2, "Shift maths",
"""You worked shifts of 4, 6 and 5.5 hours at $25 an hour.
1. Work out the total hours and the total pay.
2. Print the pay as money with 2 decimal places, e.g. `$387.50`.
3. How many whole 8-hour days is that, and how many hours are left over? (Use `//` and `%`.)""",
'''rate = 25
shift_1 = 4
shift_2 = 6
shift_3 = 5.5

total_hours = 0   # replace 0 with a calculation
total_pay = 0     # replace 0 with a calculation

print("Total hours:", total_hours)
print(f"Total pay: ${total_pay:.2f}")

# whole 8-hour days and hours left over


''',
'''rate = 25
shift_1 = 4
shift_2 = 6
shift_3 = 5.5

total_hours = shift_1 + shift_2 + shift_3
total_pay = total_hours * rate

print("Total hours:", total_hours)
print(f"Total pay: ${total_pay:.2f}")

whole_hours = int(total_hours)
print("Whole 8-hour days:", whole_hours // 8)
print("Hours left over:", whole_hours % 8)

# Year's pay for 15 hours a week at $25 an hour, 52 weeks
print(f"Year's pay: ${15 * 25 * 52:.2f}")
'''),
(2, 3, "Tidy a name",
"""A customer typed their name as `"   mei   CHEN "`.
1. Remove the extra spaces and print it in Title Case.
2. Print how many characters the tidy name has.
3. Print an order message with an f-string: `Order for Mei Chen: 2 lattes, $9.60` (a latte is $4.80).""",
'''typed = "   mei   CHEN "
lattes = 2
latte_price = 4.8

# 1. tidy name (hint: .strip() and .title())
name = typed

# 2. number of characters


# 3. the order message


''',
'''typed = "   mei   CHEN "
lattes = 2
latte_price = 4.8

name = " ".join(typed.split()).title()   # split() also removes the extra spaces in the middle
print(name)
print(len(name))
print(f"Order for {name}: {lattes} lattes, ${lattes * latte_price:.2f}")

# Your full name in capitals and its number of characters
my_name = "Sam Lee"
print(my_name.upper(), len(my_name))
'''),
(2, 4, "Ask and convert",
"""Ask the user for their hours worked and their hourly rate with `input()`.
Convert both to numbers with `float()` and print their pay with 2 decimal places.
Then print whether they worked more than 38 hours (a True/False value).""",
'''hours = input("Hours worked: ")
rate = input("Hourly rate: ")

# convert, then print the pay


# True or False: more than 38 hours?


''',
'''hours = float(input("Hours worked: "))
rate = float(input("Hourly rate: "))
print(f"Pay: ${hours * rate:.2f}")
print("More than 38 hours:", hours > 38)

# Two numbers and their total
first = float(input("First number: "))
second = float(input("Second number: "))
print("Total:", first + second)
'''),
# ── Module 3 ─────────────────────────────────────────────
(3, 1, "Open or closed?",
"""The café opens at 7 and closes at 15 (3 pm). Using the variable `hour` (0–23),
print `Open` if the café is open and `Closed` if not. Try different hours.""",
'''hour = 9

# if ... else


''',
'''hour = 9

if hour >= 7 and hour < 15:
    print("Open")
else:
    print("Closed")
'''),
(3, 2, "Stock levels",
"""Print a message about the variable `stock`:
- 0 → `Out of stock`
- 1 to 4 → `Low stock — reorder soon`
- 5 to 19 → `In stock`
- 20 or more → `Plenty in stock`""",
'''stock = 12

# if ... elif ... else


''',
'''stock = 12

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
'''),
(3, 3, "Free delivery",
"""Orders get free delivery if the total is $40 or more, OR the customer is a member — but never on a public holiday.
Print `Free delivery` or `Delivery costs $6.50`. Test all the combinations you can think of.""",
'''total = 35
is_member = True
is_public_holiday = False

# use and, or, not


''',
'''total = 35
is_member = True
is_public_holiday = False

if (total >= 40 or is_member) and not is_public_holiday:
    print("Free delivery")
else:
    print("Delivery costs $6.50")
'''),
# ── Module 4 ─────────────────────────────────────────────
(4, 1, "The menu list",
"""1. Make a list `menu` with four food items.
2. Print the first item, the last item and how many items there are.
3. Add `"Toastie"` to the end, remove one item, and print the list sorted A–Z.""",
'''menu = []   # four items in here

''',
'''menu = ["Banana bread", "Muffin", "Avocado toast", "Croissant"]
print(menu[0])
print(menu[-1])
print(len(menu))

menu.append("Toastie")
menu.remove("Muffin")
print(sorted(menu))
'''),
(4, 2, "Print the roster",
"""Loop through `staff` and print each name as `- Mel`.
Then loop through `hours` and add them up to get the total.""",
'''staff = ["Mel", "Sam", "Ali", "Priya"]
hours = [6, 5, 4, 7.5]

# for loop over staff


# add up the hours with a loop
total = 0

''',
'''staff = ["Mel", "Sam", "Ali", "Priya"]
hours = [6, 5, 4, 7.5]

for person in staff:
    print(f"- {person}")

total = 0
for h in hours:
    total += h
print("Total hours:", total)
'''),
(4, 3, "Countdown and tickets",
"""1. Use `range` to print `Ticket 1` to `Ticket 5`.
2. Use a `while` loop: start with `stock = 4` and sell one at a time, printing what's left, until it's 0.
   Then print `Sold out!`.""",
'''# 1. range


# 2. while
stock = 4

''',
'''for number in range(1, 6):
    print(f"Ticket {number}")

stock = 4
while stock > 0:
    stock -= 1
    print(f"Sold one. {stock} left")
print("Sold out!")
'''),
(4, 4, "List comprehensions",
"""1. From `prices`, make a new list with 10% GST added (rounded to 2 decimals).
2. Make a list of only the prices under $10.
3. Turn `["tea", "coffee"]` into `["TEA", "COFFEE"]`.""",
'''prices = [4.5, 12, 3.2, 18, 7.5]

with_gst = []
under_10 = []

print(with_gst)
print(under_10)
''',
'''prices = [4.5, 12, 3.2, 18, 7.5]

with_gst = [round(p * 1.1, 2) for p in prices]
under_10 = [p for p in prices if p < 10]

print(with_gst)
print(under_10)
print([d.upper() for d in ["tea", "coffee"]])
'''),
# ── Module 5 ─────────────────────────────────────────────
(5, 1, "A greeting function",
"""Write a function `greet(name)` that RETURNS `"Hi, <name>! Welcome to Corner Café."`.
Call it for two people and print the results.""",
'''def greet(name):
    pass   # replace pass with your code


print(greet("Priya"))
print(greet("Sam"))
''',
'''def greet(name):
    return f"Hi, {name}! Welcome to Corner Café."


print(greet("Priya"))
print(greet("Sam"))
'''),
(5, 2, "GST function",
"""Write `add_gst(price)` that returns the price with 10% GST, rounded to 2 decimals.
Use it to work out the total of a $20 item and a $5 item. Add a docstring.""",
'''def add_gst(price):
    pass


# Remove the # from the next two lines when your function is ready
# total = add_gst(20) + add_gst(5)
# print(total)   # should be 27.5
''',
'''def add_gst(price):
    """Return the price with 10% GST added, rounded to cents."""
    return round(price * 1.1, 2)


total = add_gst(20) + add_gst(5)
print(total)
'''),
(5, 3, "Default values",
"""Write `coffee_order(drink="Flat white", size="Regular", milk="Full cream")` that returns
a sentence like `Regular Flat white with Full cream milk`. Call it with no arguments, with one,
and with named arguments in a different order.""",
'''def coffee_order():
    pass


''',
'''def coffee_order(drink="Flat white", size="Regular", milk="Full cream"):
    return f"{size} {drink} with {milk} milk"


print(coffee_order())
print(coffee_order("Latte"))
print(coffee_order(milk="Oat", drink="Chai latte", size="Large"))
'''),
(5, 4, "Shift pay calculator",
"""Write `get_multiplier(day)` (Saturday 1.25, Sunday 1.5, other days 1) and `shift_pay(hours, day)`
(hours × $25 × multiplier). Print each shift in `week` and the week's total.
Challenge: add public holidays at 2.5 times. (Example rates only — real rates depend on your award.)""",
'''BASE_RATE = 25

def get_multiplier(day):
    pass

def shift_pay(hours, day):
    pass

week = [("Thursday", 4), ("Saturday", 6), ("Sunday", 5)]

''',
'''BASE_RATE = 25

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
'''),
# ── Module 6 ─────────────────────────────────────────────
(6, 1, "A product dictionary",
"""Make a dictionary for a product with `name`, `price` and `in_stock`.
Print a sentence using its values, change the price, add a `category` key, and print the dictionary.""",
'''product = {}

''',
'''product = {"name": "Blueberry muffin", "price": 4.75, "in_stock": True}
print(f"{product['name']} costs ${product['price']:.2f}")
product["price"] = 5
product["category"] = "Food"
print(product)
'''),
(6, 2, "Safe lookups and looping",
"""1. Print the phone number from `staff` using `.get()` with a default of `"No phone saved"`.
2. Loop through `prices` with `.items()` and print each line like `Latte: $5.00`.""",
'''staff = {"name": "Jordan", "role": "Barista"}
prices = {"Flat white": 4.5, "Latte": 5, "Chai": 5.5}

''',
'''staff = {"name": "Jordan", "role": "Barista"}
prices = {"Flat white": 4.5, "Latte": 5, "Chai": 5.5}

print(staff.get("phone", "No phone saved"))
for item, price in prices.items():
    print(f"{item}: ${price:.2f}")
'''),
(6, 3, "The roster: a list of dictionaries",
"""Using `roster`:
1. Print the names of everyone working on Saturday.
2. Print the total hours.
3. Print who has the longest shift.
4. Print everyone working more than 5 hours.""",
'''roster = [
    {"name": "Mel", "day": "Monday", "hours": 6},
    {"name": "Sam", "day": "Saturday", "hours": 5},
    {"name": "Ali", "day": "Saturday", "hours": 4},
    {"name": "Priya", "day": "Sunday", "hours": 7},
]

''',
'''roster = [
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
'''),
(6, 4, "Count the orders",
"""Count how many times each drink was ordered and print the dictionary.
Then print the most popular drink.""",
'''orders = ["Latte", "Flat white", "Latte", "Chai", "Latte", "Flat white"]
counts = {}

''',
'''orders = ["Latte", "Flat white", "Latte", "Chai", "Latte", "Flat white"]
counts = {}
for drink in orders:
    counts[drink] = counts.get(drink, 0) + 1
print(counts)
print("Most popular:", max(counts, key=counts.get))
'''),
# ── Module 7 ─────────────────────────────────────────────
(7, 1, "Save and read a CSV",
"""Write `roster` to `roster.csv` with `csv.DictWriter`, then read it back with `csv.DictReader`
and print each person's pay at $25 an hour. (Remember: everything read from a CSV is text.)""",
'''import csv

roster = [
    {"name": "Mel", "day": "Monday", "hours": 6},
    {"name": "Sam", "day": "Saturday", "hours": 5},
]

''',
'''import csv

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
'''),
(7, 2, "Don't crash",
"""Write `ask_number(question)` that keeps asking until the user types a number greater than 0,
using `try` / `except ValueError`. Use it to ask for hours and rate, then print the pay.""",
'''def ask_number(question):
    pass


''',
'''def ask_number(question):
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
'''),
(7, 3, "Using modules",
"""1. Use `random.choice` to pick today's special from a list.
2. Use `math.ceil` to work out how many 12-packs of milk you need for 50 litres.
3. Use `datetime.date.today()` to work out how many days until your birthday.""",
'''import random
import math
from datetime import date

specials = ["Banana bread", "Avocado toast", "Toastie"]

''',
'''import random
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
'''),
]
