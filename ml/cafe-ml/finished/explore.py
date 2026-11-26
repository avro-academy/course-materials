"""Get to know the café's daily data before building any models."""
import matplotlib.pyplot as plt
import pandas as pd

days = pd.read_csv("data/daily_sales.csv", parse_dates=["date"])
print(days.shape)
print(days.head(3))
print()
print(days.isna().sum()[lambda s: s > 0])                     # missing values
print()
order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
print(days.groupby("day_of_week")["customers"].mean().reindex(order).round())
print()
print("Dry days:", round(days[days["rain_mm"] == 0]["customers"].mean()),
      " Rainy days:", round(days[days["rain_mm"] > 0]["customers"].mean()))

fig, (a, b) = plt.subplots(1, 2, figsize=(12, 4))
a.plot(days["date"], days["customers"], linewidth=0.7)
a.set_title("Customers each day")
fig.autofmt_xdate()                          # tilt the dates so they fit
b.scatter(days["max_temp"], days["customers"], s=8, alpha=0.5)
b.set_title("Customers and temperature")
b.set_xlabel("Maximum temperature (°C)")
plt.savefig("explore.png", dpi=110, bbox_inches="tight")
print("Saved explore.png")
