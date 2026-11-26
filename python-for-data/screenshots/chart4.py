import pandas as pd
df = pd.read_csv("data/cafe_sales_2025_clean.csv", parse_dates=["date"])
import matplotlib.pyplot as plt

staff = df.groupby("staff")["revenue"].sum()
fig, (left, right) = plt.subplots(1, 2, figsize=(10, 4))

staff.plot(kind="bar", ax=left, color="#ff6b5b")
left.set_ylim(8800, 9500)
left.set_title("Misleading: y-axis starts at 8,800")

staff.plot(kind="bar", ax=right, color="#14b8a6")
right.set_ylim(0, 10000)
right.set_title("Honest: y-axis starts at 0")

for ax in (left, right):
    ax.set_xlabel("")
    ax.set_ylabel("Revenue ($)")
plt.tight_layout()
plt.savefig("honest_vs_misleading.png", dpi=150)
