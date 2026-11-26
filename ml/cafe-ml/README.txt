Corner Café machine learning files
Course: Machine Learning Basics with Python (Avro Academy)

data/       the café's data (made up for the course, but it behaves like real data)
  daily_sales.csv      two years of days: weather, day of the week, holidays, customers and iced drinks sold
  loyalty_members.csv  1,200 loyalty members' habits, and whether they came back the next month
  reviews.csv          775 customer reviews with their star rating
finished/   every finished script from the lessons, to compare with yours

Set up (in this folder):
  python -m venv .venv
  source .venv/bin/activate          (Windows PowerShell: .venv\Scripts\activate)
  pip install scikit-learn pandas matplotlib

Run your scripts from this folder, so data/ is found:
  python first_model.py
To run a finished one:  python finished/first_model.py

Your numbers can differ slightly from the lessons with other library versions
(the lessons used scikit-learn 1.9.1 and pandas 3.1).
