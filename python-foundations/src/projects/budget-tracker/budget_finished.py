"""Pay and budget tracker (finished version) — Python Foundations, Module 8."""
import csv
import os

FILE = "budget.csv"


def save(entries):
    with open(FILE, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["type", "description", "amount"])
        writer.writeheader()
        writer.writerows(entries)


def load():
    if not os.path.exists(FILE):
        return []
    with open(FILE, newline="") as file:
        return [{"type": row["type"], "description": row["description"], "amount": float(row["amount"])}
                for row in csv.DictReader(file)]


def ask_amount():
    """Keep asking until the user types an amount greater than 0."""
    while True:
        try:
            amount = float(input("Amount: $").strip())
            if amount > 0:
                return round(amount, 2)
            print("The amount must be more than 0.")
        except ValueError:
            print("Please type a number, like 12.50")


def add(entries, kind):
    description = input("Description: ").strip() or ("Pay" if kind == "income" else "Spending")
    amount = ask_amount()
    entries.append({"type": kind, "description": description, "amount": amount})
    save(entries)
    print(f"Saved: {description} ${amount:.2f}\n")


def summary(entries):
    if not entries:
        print("Nothing saved yet.\n")
        return
    for e in entries:
        sign = "+" if e["type"] == "income" else "-"
        print(f"  {sign} {e['description']:<20} ${e['amount']:>8.2f}")
    income = sum(e["amount"] for e in entries if e["type"] == "income")
    spending = sum(e["amount"] for e in entries if e["type"] == "expense")
    print(f"Income:   ${income:.2f}")
    print(f"Spending: ${spending:.2f}")
    print(f"Left:     ${income - spending:.2f}\n")


def main():
    entries = load()
    print(f"Pay and budget tracker — {len(entries)} saved entries")
    while True:
        print("1. Add pay   2. Add spending   3. Summary   4. Quit")
        choice = input("Choose: ").strip()
        if choice == "1":
            add(entries, "income")
        elif choice == "2":
            add(entries, "expense")
        elif choice == "3":
            summary(entries)
        elif choice == "4":
            print("Bye!")
            break
        else:
            print("Please choose 1, 2, 3 or 4.")


if __name__ == "__main__":
    main()
