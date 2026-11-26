"""Runs the code from the lessons against the starter data and checks the printed output matches the lessons."""
import contextlib, io, os, sys
import pandas as pd
pd.set_option('display.width', 120)
os.chdir(sys.argv[1])
import matplotlib; matplotlib.use('Agg')
CHECKS = []
def check(code, expected):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf): exec(code, {})
    got = buf.getvalue().strip()
    ok = [l.rstrip() for l in got.splitlines()] == [l.rstrip() for l in expected.strip().splitlines()]
    CHECKS.append(ok)
    if not ok: print('MISMATCH\n--- code:\n' + code.strip()[:300] + '\n--- expected:\n' + expected.strip() + '\n--- got:\n' + got + '\n')
RAW = 'import pandas as pd\ndf = pd.read_csv("data/cafe_sales_2025.csv")\n'
CLEAN = 'import pandas as pd\ndf = pd.read_csv("data/cafe_sales_2025_clean.csv", parse_dates=["date"])\n'
check('''import csv
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
print(f"1 January: {orders} order lines, ${total:.2f}")''', '1 January: 14 order lines, $113.80')
check(RAW + '''day = df[df["date"] == "01/01/2025"].dropna(subset=["quantity"])
price = day["unit_price"].str.replace("$", "", regex=False).astype(float)
print(f"1 January: {len(day)} order lines, ${(day['quantity'] * price).sum():.2f}")''', '1 January: 14 order lines, $113.80')
check(RAW + 'print(df.shape)\nprint(df.columns.tolist())', "(5865, 9)\n['order_id', 'date', 'time', 'item', 'category', 'quantity', 'unit_price', 'payment', 'staff']")
check(RAW + 'print(df[["date", "item", "quantity", "unit_price"]].head())', '''         date                   item  quantity unit_price
0  01/01/2025             Chai latte       1.0      $5.20
1  01/01/2025  English breakfast tea       2.0      $4.00
2  01/01/2025          Hot chocolate       2.0      $5.00
3  01/01/2025           Orange juice       1.0        5.5
4  01/01/2025            Lemon slice       1.0      $4.50''')
check(RAW + 'print(df.isna().sum())', '''order_id       0
date           0
time           0
item           0
category       0
quantity      87
unit_price     0
payment       58
staff          0
dtype: int64''')
check(RAW + 'print(df["payment"].value_counts(dropna=False))', '''payment
Card    4776
Cash     796
card     173
CARD      62
NaN       58
Name: count, dtype: int64''')
check(RAW + 'print(df["quantity"].describe())', '''count    5778.000000
mean        1.458463
std         1.737416
min         1.000000
25%         1.000000
50%         1.000000
75%         2.000000
max       120.000000
Name: quantity, dtype: float64''')
check(RAW + '''big = df[df["quantity"] >= 4]
print(len(big))
sam_cash = df[(df["staff"] == "Sam") & (df["payment"] == "Cash")]
print(len(sam_cash))
coffee_or_tea = df[df["category"].isin(["Coffee", "Tea"])]
print(len(coffee_or_tea))''', '187\n154\n3416')
check(RAW + 'lattes = df[df["item"].str.contains("latte", case=False)]\nprint(lattes["item"].value_counts())', '''item
Latte          835
Chai latte     299
 chai latte     20
Chai Latte      20
Name: count, dtype: int64''')
check(RAW + 'print(df.loc[df["quantity"] > 10, ["order_id", "date", "item", "quantity"]])', '''      order_id        date        item  quantity
2354     12346  01/06/2025  Cappuccino     120.0''')
check('import pandas as pd\nproducts = pd.read_csv("data/products.csv")\nprint(products.sort_values("cost_price", ascending=False).head(3))', '''                      item  cost_price
11             Veggie wrap         3.9
10  Ham and cheese toastie         3.2
8             Orange juice         1.9''')
check('import pandas as pd\nproducts = pd.read_csv("data/products.csv")\nproducts["cost_with_gst"] = (products["cost_price"] * 1.1).round(2)\nproducts["expensive"] = products["cost_price"] > 2\nprint(products.head(4))', '''         item  cost_price  cost_with_gst  expensive
0  Flat white        1.10           1.21      False
1       Latte        1.15           1.26      False
2  Cappuccino        1.10           1.21      False
3  Long black        0.80           0.88      False''')
check(RAW + 'print("Duplicate rows:", df.duplicated().sum())\nprint("Item spellings:", df["item"].nunique())\nprint(sorted(df["item"].unique())[:6])', '''Duplicate rows: 18
Item spellings: 21
[' chai latte', 'Banana Bread', 'Banana bread', 'Cappuccino', 'Chai Latte', 'Chai latte']''')
check(RAW + 'print(df["unit_price"].head(3).tolist())\ndf["unit_price"] = df["unit_price"].str.replace("$", "", regex=False).astype(float)\nprint(df["unit_price"].head(3).tolist())\nprint(df["unit_price"].mean().round(2))', "['$5.20', '$4.00', '$5.00']\n[5.2, 4.0, 5.0]\n5.5")
check(RAW + 'df["date"] = pd.to_datetime(df["date"], format="%d/%m/%Y")\nprint(df["date"].min().date(), "to", df["date"].max().date())\nprint(df["date"].dt.day_name().iloc[0])', '2025-01-01 to 2025-12-31\nWednesday')
check(RAW + 'df["item"] = df["item"].str.strip().str.capitalize()\ndf["payment"] = df["payment"].str.title()\nprint(df["item"].nunique())\nprint(df["payment"].value_counts(dropna=False).to_dict())', "14\n{'Card': 5011, 'Cash': 796, nan: 58}")
check(open('scripts/clean_sales.py').read(), '5865 rows in, 5759 rows out\nTotal revenue: $45,599.50')
check(CLEAN + 'print(df.groupby("category")["revenue"].sum().sort_values(ascending=False))', '''category
Coffee    18902.4
Food      16564.0
Drinks     6391.5
Tea        3741.6
Name: revenue, dtype: float64''')
check(CLEAN + 'top = df.groupby("item")["quantity"].sum().sort_values(ascending=False)\nprint(top.head(5))', '''item
Flat white                1495
Latte                     1145
Cappuccino                 822
Banana bread               650
Ham and cheese toastie     567
Name: quantity, dtype: int64''')
check(CLEAN + 'summary = df.groupby("staff").agg(\n    lines=("order_id", "count"),\n    revenue=("revenue", "sum"),\n    average=("revenue", "mean"),\n).round(2)\nprint(summary)', '''        lines  revenue  average
staff
Ali      1174   9195.5     7.83
Jordan   1157   9033.2     7.81
Mel      1185   9451.1     7.98
Priya    1124   8848.5     7.87
Sam      1119   9071.2     8.11''')
check(CLEAN + 'monthly = df.groupby(df["date"].dt.month)["revenue"].sum().round(2)\nprint(monthly)', '''date
1     3355.9
2     3292.5
3     3812.2
4     3463.4
5     3963.2
6     4296.0
7     4567.5
8     4539.7
9     3450.1
10    3563.5
11    4128.6
12    3166.9
Name: revenue, dtype: float64''')
check(CLEAN + 'order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]\nby_day = df.groupby(df["date"].dt.day_name())["revenue"].sum().reindex(order).round(2)\nprint(by_day)', '''date
Monday       5446.7
Tuesday      5455.7
Wednesday    5784.6
Thursday     5386.9
Friday       5902.9
Saturday     8776.6
Sunday       8846.1
Name: revenue, dtype: float64''')
check(CLEAN + 'df["hour"] = df["time"].str.slice(0, 2).astype(int)\nprint(df.groupby("hour")["order_id"].count().idxmax())', '8')
check(CLEAN + '''products = pd.read_csv("data/products.csv")
merged = df.merge(products, on="item", how="left")
merged["profit"] = merged["revenue"] - merged["quantity"] * merged["cost_price"]
print(merged["cost_price"].isna().sum())
profit = merged.groupby("item")["profit"].sum().sort_values(ascending=False).round(2)
print(profit.head(5))''', '''0
item
Flat white                5531.50
Latte                     4179.25
Ham and cheese toastie    3572.10
Cappuccino                3041.40
Veggie wrap               2754.80
Name: profit, dtype: float64''')
check(CLEAN + 'df["quarter"] = "Q" + df["date"].dt.quarter.astype(str)\ntable = df.pivot_table(index="category", columns="quarter", values="revenue", aggfunc="sum").round(2)\nprint(table)', '''quarter       Q1      Q2      Q3      Q4
category
Coffee    4518.6  4947.0  4849.8  4587.0
Drinks    1371.5  1538.0  1956.0  1526.0
Food      3618.5  4242.0  4779.5  3924.0
Tea        952.0   995.6   972.0   822.0''')
check(CLEAN + 'print(pd.crosstab(df["category"], df["payment"]))', '''payment   Card  Cash  Unknown
category
Coffee    2408   366       26
Drinks     686   106        8
Food      1368   225       16
Tea        461    82        7''')
check(CLEAN + '''by_category = df.groupby("category")["revenue"].sum().round(2).reset_index()
by_month = df.groupby(df["date"].dt.month)["revenue"].sum().round(2).reset_index()
by_month.columns = ["month", "revenue"]
with pd.ExcelWriter("/tmp/cafe_report_2025.xlsx") as writer:
    by_category.to_excel(writer, sheet_name="By category", index=False)
    by_month.to_excel(writer, sheet_name="By month", index=False)
check = pd.read_excel("/tmp/cafe_report_2025.xlsx", sheet_name=None)
print(list(check.keys()))
print(check["By category"])''', """['By category', 'By month']
  category  revenue
0   Coffee  18902.4
1   Drinks   6391.5
2     Food  16564.0
3      Tea   3741.6""")
check(CLEAN + '''order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
print(f"Revenue:       ${df['revenue'].sum():,.2f}")
print(f"Order lines:   {len(df):,}")
print(f"Best month:    {df.groupby(df['date'].dt.month_name())['revenue'].sum().idxmax()}")
print(f"Best weekday:  {df.groupby(df['date'].dt.day_name())['revenue'].sum().reindex(order).idxmax()}")
print(f"Card payments: {(df['payment'] == 'Card').mean():.0%}")''', '''Revenue:       $45,599.50
Order lines:   5,759
Best month:    July
Best weekday:  Sunday
Card payments: 85%''')
print(f'{sum(CHECKS)}/{len(CHECKS)} lesson outputs match')
# shape checks for the charts' captions
df = pd.read_csv("data/cafe_sales_2025_clean.csv", parse_dates=["date"])
df["hour"] = df["time"].str.slice(0, 2).astype(int)
print(df.groupby("hour")["order_id"].count().to_dict())
