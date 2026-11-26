import pandas as pd
df = pd.read_csv("data/cafe_sales_2025_clean.csv", parse_dates=["date"])
import matplotlib.pyplot as plt

df["hour"] = df["time"].str.slice(0, 2).astype(int)
ax = df["hour"].plot(kind="hist", bins=range(7, 17), color="#ffb627", edgecolor="white")
ax.set_title("Order lines by hour of the day")
ax.set_xlabel("Hour (24-hour time)")
ax.set_ylabel("Number of order lines")
plt.tight_layout()
plt.savefig("orders_by_hour.png", dpi=150)
