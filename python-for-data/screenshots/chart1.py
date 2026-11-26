import pandas as pd
df = pd.read_csv("data/cafe_sales_2025_clean.csv", parse_dates=["date"])
import matplotlib.pyplot as plt

by_cat = df.groupby("category")["revenue"].sum().sort_values()
ax = by_cat.plot(kind="barh", color="#14b8a6")
ax.set_title("Revenue by category, 2025")
ax.set_xlabel("Revenue ($)")
ax.set_ylabel("")
plt.tight_layout()
plt.savefig("revenue_by_category.png", dpi=150)
