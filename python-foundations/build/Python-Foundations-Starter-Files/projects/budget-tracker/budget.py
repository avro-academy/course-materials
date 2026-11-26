"""Pay and budget tracker — Python Foundations, Module 8.

Follow the steps in the lesson "Project: pay and budget tracker".
Run it with:  python budget.py
Your entries are saved in budget.csv next to this file (open it in Excel or Google Sheets).
Stuck? Compare with budget_finished.py.
"""
import csv
import os

FILE = "budget.csv"


def save(entries):
    """Write every entry to the CSV file (columns: type, description, amount)."""
    # TODO: use csv.DictWriter, writeheader() and writerows()
    pass


def load():
    """Return the saved entries, or an empty list if there's no file yet."""
    # TODO: if the file doesn't exist return [] (hint: os.path.exists)
    # TODO: read it with csv.DictReader and turn "amount" back into a float
    return []


def ask_amount():
    """Keep asking until the user types an amount greater than 0."""
    # TODO: while True + try/except ValueError (Module 7)
    pass


def add(entries, kind):
    """Ask for a description and amount, add the entry and save. kind is "income" or "expense"."""
    # TODO
    pass


def summary(entries):
    """Print every entry, then total income, total spending and what's left."""
    # TODO
    pass


def main():
    entries = load()
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
