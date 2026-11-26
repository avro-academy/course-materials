# Prints Alex's monthly money summary from budget.db.
#   python budget_report.py
import sqlite3

con = sqlite3.connect("budget.db")
con.row_factory = sqlite3.Row  # rows act like dictionaries: row["month"]

rows = con.execute("""
    SELECT strftime('%Y-%m', day) AS month,
           sum(CASE WHEN amount > 0 THEN amount ELSE 0 END) AS money_in,
           sum(CASE WHEN amount < 0 THEN -amount ELSE 0 END) AS money_out
    FROM transactions
    GROUP BY month
    ORDER BY month
""").fetchall()

print("Month     Money in   Money out   Left over")
for row in rows:
    left = row["money_in"] - row["money_out"]
    print(f"{row['month']}  {row['money_in']:9.2f}  {row['money_out']:10.2f}  {left:10.2f}")

con.close()
