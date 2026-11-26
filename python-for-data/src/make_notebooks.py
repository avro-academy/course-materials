"""Builds notebooks/module-1..6.ipynb, notebooks/capstone.ipynb and the matching solutions/*.ipynb, then runs every solution cell."""
import json, os, sys, contextlib, io
B = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'build', 'starter')
SETUP = '''# Run this cell first.
# In Colab: upload Python-for-Data-Starter-Files.zip to the Files panel (the zip itself), then run this.
# On your own computer it just checks the files are there.
import os, zipfile
from pathlib import Path
for z in sorted(Path(".").glob("Python-for-Data-Starter-Files*.zip")):
    if not Path("Python-for-Data-Starter-Files").exists():
        zipfile.ZipFile(z).extractall()
if Path("Python-for-Data-Starter-Files").is_dir():
    os.chdir("Python-for-Data-Starter-Files")
if not Path("data").is_dir() and Path("../data").is_dir():
    os.chdir("..")
needed = ["data/cafe_sales_2025.csv", "data/cafe_sales_2025_clean.csv", "data/products.csv", "data/rosters/roster_week_01.csv"]
missing = [f for f in needed if not Path(f).exists()]
print("All files found!" if not missing else f"Missing: {missing}. Upload the zip, wait for it to finish, and run this cell again.")'''
LOAD_RAW = 'import pandas as pd\ndf = pd.read_csv("data/cafe_sales_2025.csv")'
LOAD_CLEAN = 'import pandas as pd\nimport matplotlib.pyplot as plt\ndf = pd.read_csv("data/cafe_sales_2025_clean.csv", parse_dates=["date"])'
# each notebook: title, intro, list of (markdown, starter code, solution code)
NB = {
'module-1': ('Module 1: Data with Python', 'Plain Python first, then the same question in pandas.', [
  ('### Try it: the lesson example\nRun this cell. It adds up the sales on 1 January with plain Python.', '''import csv
total = 0
orders = 0
with open("data/cafe_sales_2025.csv", newline="") as file:
    for row in csv.DictReader(file):
        if row["date"] != "01/01/2025":
            continue
        if row["quantity"] == "":
            continue
        price = float(row["unit_price"].replace("$", ""))
        total += int(row["quantity"]) * price
        orders += 1
print(f"1 January: {orders} order lines, ${total:.2f}")''', None),
  ('### Exercise: count the cash payments\nUsing plain Python and the `csv` module, count how many rows have `payment` equal to `"Cash"`.', '''import csv
cash = 0
with open("data/cafe_sales_2025.csv", newline="") as file:
    for row in csv.DictReader(file):
        # your code here
        pass
print("Cash payments:", cash)''', '''import csv
cash = 0
with open("data/cafe_sales_2025.csv", newline="") as file:
    for row in csv.DictReader(file):
        if row["payment"] == "Cash":
            cash += 1
print("Cash payments:", cash)   # 796'''),
  ('### Bonus\nNow do it with pandas in one line. Hint: `value_counts()` or a filter and `len()`.', LOAD_RAW + '\n# your code here', LOAD_RAW + '\nprint(len(df[df["payment"] == "Cash"]))   # 796'),
]),
'module-2': ('Module 2: pandas basics', 'Load, explore, filter, sort and add columns.', [
  ('### Exercise 1: load and look\nLoad `data/products.csv` into a DataFrame called `products`. Print its shape, its column names and the first 5 rows.', 'import pandas as pd\n# your code here', 'import pandas as pd\nproducts = pd.read_csv("data/products.csv")\nprint(products.shape)              # (14, 2)\nprint(products.columns.tolist())\nprint(products.head())'),
  ('### Exercise 2: explore\n1. Run `df.info()`. Which column has missing values?\n2. How many order lines did each staff member serve? (`value_counts`)\n3. Run `df["item"].unique()`. How many ways is "Flat white" written?', LOAD_RAW + '\n# your code here', LOAD_RAW + '''
df.info()                               # quantity and payment have missing values
print(df["staff"].value_counts())
print(sorted(i for i in df["item"].unique() if "flat" in i.lower()))   # 4 ways: 'Flat White', 'Flat white', 'Flat white ', 'flat white\''''),
  ('### Exercise 3: filter\n1. How many order lines were for a Long black with a quantity of 2 or more?\n2. Show every order Priya served on 25/12/2025 (columns `time`, `item`, `quantity`).', LOAD_RAW + '\n# your code here', LOAD_RAW + '''
print(len(df[(df["item"] == "Long black") & (df["quantity"] >= 2)]))
print(df.loc[(df["staff"] == "Priya") & (df["date"] == "25/12/2025"), ["time", "item", "quantity"]])'''),
  ('### Exercise 4: sort and new columns\nIn `products`, add a column `margin_note` that is True when the cost price is under $1. Then sort the products from cheapest to most expensive to make.', 'import pandas as pd\nproducts = pd.read_csv("data/products.csv")\n# your code here', 'import pandas as pd\nproducts = pd.read_csv("data/products.csv")\nproducts["margin_note"] = products["cost_price"] < 1\nprint(products.sort_values("cost_price"))'),
]),
'module-3': ('Module 3: Cleaning messy data', 'Find the problems, fix them in code, save a clean file.', [
  ('### The checklist\nRun the cleaning checklist on the raw data.', LOAD_RAW + '\nprint("Duplicate rows:", df.duplicated().sum())\nprint(df.isna().sum())\nprint("Item spellings:", df["item"].nunique())\nprint(df["quantity"].describe())', None),
  ('### Exercise 1: fix the types\nConvert `unit_price` to numbers and `date` to real dates (day/month/year). Then answer: what day of the week was 25 December 2025, and what was the most expensive unit price?', LOAD_RAW + '\n# your code here', LOAD_RAW + '''
df["unit_price"] = df["unit_price"].str.replace("$", "", regex=False).astype(float)
df["date"] = pd.to_datetime(df["date"], format="%d/%m/%Y")
print(pd.Timestamp("2025-12-25").day_name())   # Thursday
print(df["unit_price"].max())                  # 11.0 (Veggie wrap)'''),
  ('### The complete cleaning script\nThis is the script from the lesson (also in `scripts/clean_sales.py`). Run it.', open(os.path.join(B, 'scripts', 'clean_sales.py')).read().split('"""', 2)[2].strip(), None),
  ('### Exercise 2: check the clean file\nLoad `data/cafe_sales_2025_clean.csv` and check: no duplicates, no missing quantities, 14 items, and payment is only Card, Cash or Unknown.', 'import pandas as pd\n# your code here', '''import pandas as pd
clean = pd.read_csv("data/cafe_sales_2025_clean.csv")
print(clean.duplicated().sum())          # 0
print(clean["quantity"].isna().sum())    # 0
print(clean["item"].nunique())           # 14
print(clean["payment"].unique())'''),
]),
'module-4': ('Module 4: Analysing', 'groupby, dates, merge and pivot tables.', [
  ('### Exercise 1: groupby\n1. Which 5 items earned the most revenue?\n2. What is the average quantity per order line for each category?', LOAD_CLEAN + '\n# your code here', LOAD_CLEAN + '''
print(df.groupby("item")["revenue"].sum().sort_values(ascending=False).head(5))
print(df.groupby("category")["quantity"].mean().round(2))'''),
  ('### Exercise 2: when are we busiest?\nCount order lines by hour of the day and by day of the week. Is it what you expected?', LOAD_CLEAN + '\n# your code here', LOAD_CLEAN + '''
df["hour"] = df["time"].str.slice(0, 2).astype(int)
print(df.groupby("hour")["order_id"].count())
order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
print(df.groupby(df["date"].dt.day_name())["order_id"].count().reindex(order))'''),
  ('### Exercise 3: merge\nMerge in `products.csv`, work out profit, and find which category has the best margin (profit ÷ revenue).', LOAD_CLEAN + '\nproducts = pd.read_csv("data/products.csv")\n# your code here', LOAD_CLEAN + '''
products = pd.read_csv("data/products.csv")
merged = df.merge(products, on="item", how="left")
merged["profit"] = merged["revenue"] - merged["quantity"] * merged["cost_price"]
by_cat = merged.groupby("category")[["revenue", "profit"]].sum()
by_cat["margin"] = (by_cat["profit"] / by_cat["revenue"]).round(3)
print(by_cat.sort_values("margin", ascending=False))   # Tea has the best margin'''),
  ('### Exercise 4: pivot table\nMake a pivot table of revenue with staff as rows and day of the week as columns.', LOAD_CLEAN + '\n# your code here', LOAD_CLEAN + '''
df["day"] = df["date"].dt.day_name()
order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
print(df.pivot_table(index="staff", columns="day", values="revenue", aggfunc="sum").reindex(columns=order).round(0))'''),
]),
'module-5': ('Module 5: Visualising', 'Bar, line and histogram charts that tell the truth.', [
  ('### Exercise 1: top 10 items\nMake a horizontal bar chart of the top 10 items by quantity sold, with a title and axis labels. Save it as `top_items.png`.', LOAD_CLEAN + '\n# your code here', LOAD_CLEAN + '''
top = df.groupby("item")["quantity"].sum().sort_values().tail(10)
ax = top.plot(kind="barh", color="#14b8a6")
ax.set_title("Top 10 items by quantity, 2025")
ax.set_xlabel("Quantity sold")
ax.set_ylabel("")
plt.tight_layout()
plt.savefig("top_items.png", dpi=150)'''),
  ('### Exercise 2: choose the chart\n1. Draw a line chart of revenue by week of the year (`df["date"].dt.isocalendar().week`).\n2. Draw a histogram of `revenue` per order line. What does its shape tell you?', LOAD_CLEAN + '\n# your code here', LOAD_CLEAN + '''
weekly = df.groupby(df["date"].dt.isocalendar().week)["revenue"].sum()
ax = weekly.plot(kind="line", color="#0b1f3a")
ax.set_title("Revenue by week, 2025"); ax.set_xlabel("Week of the year"); ax.set_ylabel("Revenue ($)")
ax.set_ylim(0, weekly.max() * 1.1)
plt.tight_layout(); plt.show()
ax = df["revenue"].plot(kind="hist", bins=20, color="#ffb627", edgecolor="white")
ax.set_title("Revenue per order line"); ax.set_xlabel("Revenue ($)"); ax.set_ylabel("Order lines")
plt.tight_layout(); plt.show()   # most lines are under $12: one or two items'''),
]),
'module-6': ('Module 6: Automating everyday tasks', 'Combine many files and write reports.', [
  ('### Exercise 1: combine the rosters\nCombine every file in `data/rosters`, add a `week` column, and show the total hours for each week.', 'import pandas as pd\nfrom pathlib import Path\n# your code here', '''import pandas as pd
from pathlib import Path
frames = []
for f in sorted(Path("data/rosters").glob("roster_week_*.csv")):
    week = pd.read_csv(f)
    week["week"] = int(f.stem.split("_")[-1])
    frames.append(week)
roster = pd.concat(frames, ignore_index=True)
print(roster.groupby("week")["hours"].sum())'''),
  ('### Project: weekly roster hours report\nThe function from the lesson (also in `scripts/roster_report.py`).', open(os.path.join(B, 'scripts', 'roster_report.py')).read().split('"""', 2)[2].strip(), None),
  ('### Make it yours\nFlag anyone who worked more than 38 hours in a single week.', '# your code here', '''import pandas as pd
from pathlib import Path
frames = [pd.read_csv(f).assign(week=int(f.stem.split("_")[-1])) for f in sorted(Path("data/rosters").glob("roster_week_*.csv"))]
roster = pd.concat(frames, ignore_index=True)
weekly = roster.groupby(["name", "week"])["hours"].sum()
print(weekly[weekly > 38] if (weekly > 38).any() else "Nobody worked more than 38 hours in a week.")'''),
]),
'capstone': ('Capstone: a year at Corner Café', 'You are the café\'s new data person. The owner asks: "How did we go in 2025, and what should we change next year?" Work through each step, then write 3 to 5 findings.', [
  ('### Step 1: clean\nUse the clean file (made by `scripts/clean_sales.py`). Write down every cleaning decision in a markdown cell.', LOAD_CLEAN + '\nproducts = pd.read_csv("data/products.csv")\nprint(df.shape)', None),
  ('### Step 2: headline numbers', LOAD_CLEAN + '''
order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
print(f"Revenue:       ${df['revenue'].sum():,.2f}")
print(f"Order lines:   {len(df):,}")
print(f"Best month:    {df.groupby(df['date'].dt.month_name())['revenue'].sum().idxmax()}")
print(f"Best weekday:  {df.groupby(df['date'].dt.day_name())['revenue'].sum().reindex(order).idxmax()}")
print(f"Card payments: {(df['payment'] == 'Card').mean():.0%}")''', None),
  ('### Step 3: what sells\nTop items by quantity and by profit.', LOAD_CLEAN + '\nproducts = pd.read_csv("data/products.csv")\n# your code here', LOAD_CLEAN + '''
products = pd.read_csv("data/products.csv")
m = df.merge(products, on="item", how="left")
m["profit"] = m["revenue"] - m["quantity"] * m["cost_price"]
print(m.groupby("item")["quantity"].sum().sort_values(ascending=False).head(5))
print(m.groupby("item")["profit"].sum().sort_values(ascending=False).head(5).round(2))'''),
  ('### Step 4: when\nBusiest months, weekdays and hours.', LOAD_CLEAN + '\n# your code here', LOAD_CLEAN + '''
df["hour"] = df["time"].str.slice(0, 2).astype(int)
print(df.groupby(df["date"].dt.month)["revenue"].sum())
print(df.groupby(df["date"].dt.day_name())["revenue"].sum().sort_values(ascending=False))
print(df.groupby("hour")["order_id"].count())'''),
  ('### Step 5: how people pay', LOAD_CLEAN + '\n# your code here', LOAD_CLEAN + '\nprint(df["payment"].value_counts(normalize=True).round(3))'),
  ('### Step 6: at least three honest charts\nBars start at zero, titles say what and when, axes are labelled.', LOAD_CLEAN + '\n# your code here', LOAD_CLEAN + '''
fig, axes = plt.subplots(1, 3, figsize=(15, 4))
df.groupby("category")["revenue"].sum().sort_values().plot(kind="barh", ax=axes[0], color="#14b8a6", title="Revenue by category, 2025")
m = df.groupby(df["date"].dt.month)["revenue"].sum()
m.plot(kind="line", marker="o", ax=axes[1], color="#0b1f3a", title="Monthly revenue, 2025"); axes[1].set_ylim(0, m.max() * 1.1)
order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
df.groupby(df["date"].dt.day_name())["revenue"].sum().reindex(order).plot(kind="bar", ax=axes[2], color="#ff6b5b", title="Revenue by weekday, 2025")
for ax in axes: ax.set_ylabel("Revenue ($)" if ax is not axes[0] else ""); ax.set_xlabel("")
plt.tight_layout(); plt.savefig("capstone_charts.png", dpi=150)'''),
  ('### Step 7: findings\nWrite 3 to 5 findings here. Each one: a number, what it means, and a recommendation.\n\n1. \n2. \n3. ', None, None),
]),
}
def nb(cells):
    return {'cells': cells, 'metadata': {'colab': {'provenance': []}, 'kernelspec': {'display_name': 'Python 3', 'name': 'python3'}, 'language_info': {'name': 'python'}}, 'nbformat': 4, 'nbformat_minor': 0}
md = lambda t: {'cell_type': 'markdown', 'metadata': {}, 'source': t.splitlines(True)}
code = lambda t: {'cell_type': 'code', 'execution_count': None, 'metadata': {}, 'outputs': [], 'source': t.splitlines(True)}
os.makedirs(os.path.join(B, 'notebooks'), exist_ok=True); os.makedirs(os.path.join(B, 'solutions'), exist_ok=True)
fails = 0
for name, (title, intro, steps) in NB.items():
    for kind in ('notebooks', 'solutions'):
        cells = [md(f'# {title}' + (' (solutions)' if kind == 'solutions' else '') + f'\n\nPython for Data: Clean, Analyse and Visualise · Avro Academy\n\n{intro}'), code(SETUP)]
        for text, starter, sol in steps:
            cells.append(md(text))
            if starter is not None or sol is not None:
                cells.append(code(sol if (kind == 'solutions' and sol) else starter))
        fn = name + ('-solutions' if kind == 'solutions' else '') + '.ipynb'
        json.dump(nb(cells), open(os.path.join(B, kind, fn), 'w'), indent=1)
        if kind == 'solutions':  # run every code cell
            cwd = os.getcwd(); os.chdir(B)
            import matplotlib; matplotlib.use('Agg')
            g = {}
            for c in cells:
                if c['cell_type'] == 'code':
                    try:
                        with contextlib.redirect_stdout(io.StringIO()): exec(''.join(c['source']), g)
                    except Exception as e:
                        fails += 1; print('FAIL', fn, repr(e), ''.join(c['source'])[:120])
            os.chdir(cwd)
print('notebooks built; failures:', fails)
