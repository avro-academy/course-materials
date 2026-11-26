# Adds one transaction to budget.db.
#   python add_expense.py 2026-04-02 "QUICKBITE TAKEAWAY" -12.50
import sqlite3
import sys

day, description, amount = sys.argv[1], sys.argv[2], float(sys.argv[3])

with sqlite3.connect("budget.db") as con:  # commits when the block ends (or rolls back on an error)
    con.execute(
        "INSERT INTO transactions (day, description, amount) VALUES (?, ?, ?)",  # ? = a parameter, never glued-in text
        (day, description, amount),
    )
    total = con.execute(
        "SELECT round(sum(amount), 2) FROM transactions WHERE strftime('%Y-%m', day) = strftime('%Y-%m', ?)",
        (day,),
    ).fetchone()[0]

print(f"Added {description} ({amount:.2f}) on {day}.")
print(f"Total for that month so far: {total:.2f}")
