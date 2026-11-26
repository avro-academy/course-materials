import pandas as pd
df = pd.read_csv("data/cafe_sales_2025_clean.csv", parse_dates=["date"])
import matplotlib.pyplot as plt

monthly = df.groupby(df["date"].dt.month)["revenue"].sum()
ax = monthly.plot(kind="line", marker="o", color="#0b1f3a")
ax.set_title("Monthly revenue, 2025")
ax.set_xlabel("Month")
ax.set_ylabel("Revenue ($)")
ax.set_xticks(range(1, 13))
ax.set_ylim(0, monthly.max() * 1.1)
plt.tight_layout()
plt.savefig("monthly_revenue.png", dpi=150)
