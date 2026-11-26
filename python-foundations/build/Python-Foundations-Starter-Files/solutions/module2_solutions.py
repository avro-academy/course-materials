# Module 2: Values and variables — solutions

# ── Task 1: Your café in variables ────────────────────────────

cafe_name = "Corner Café"
tables = 8
coffee_price = 4.5
customers = 10

print(cafe_name)
print(tables)
print(coffee_price)

customers += 4
print(customers)

# ── Task 2: Shift maths ───────────────────────────────────────

rate = 25
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

# ── Task 3: Tidy a name ───────────────────────────────────────

typed = "   mei   CHEN "
lattes = 2
latte_price = 4.8

name = " ".join(typed.split()).title()   # split() also removes the extra spaces in the middle
print(name)
print(len(name))
print(f"Order for {name}: {lattes} lattes, ${lattes * latte_price:.2f}")

# Your full name in capitals and its number of characters
my_name = "Sam Lee"
print(my_name.upper(), len(my_name))

# ── Task 4: Ask and convert ───────────────────────────────────

hours = float(input("Hours worked: "))
rate = float(input("Hourly rate: "))
print(f"Pay: ${hours * rate:.2f}")
print("More than 38 hours:", hours > 38)

# Two numbers and their total
first = float(input("First number: "))
second = float(input("Second number: "))
print("Total:", first + second)
