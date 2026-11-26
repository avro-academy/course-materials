BUDGET: starter files
Avro Academy · SQLite in Practice: Track Your Spending

  everyday-2026-01-to-02.csv   Alex's bank download for January and February
  everyday-2026-02-to-03.csv   the second download: February (again) and March
  budget_report.py             Module 5: prints the monthly summary from budget.db
  add_expense.py               Module 5: adds one transaction, safely
  solutions/                   answers to every "Try it" question, one file per module

HOW TO START
  Unzip this into a folder called budget and open a terminal there.
  sqlite3 budget.db            then follow Module 2 to import the CSV files

  Open the CSV files in a text editor, not Excel: Excel changes how the dates look,
  and if you save from Excel the import won't match the course.

  The Python scripts need budget.db from Modules 2 to 4 in the same folder:
    python3 budget_report.py                                  (Windows: python)
    python3 add_expense.py 2026-04-02 "QUICKBITE TAKEAWAY" -12.50

Alex, the shops and the bank are made up.
