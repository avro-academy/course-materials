"""Your first machine learning model: learn how hot days and iced drinks go together."""
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LinearRegression

days = pd.read_csv("data/daily_sales.csv").dropna()

X = days[["max_temp"]]       # what we know (a table, even with one column)
y = days["iced_drinks"]      # what we want to predict

model = LinearRegression()
model.fit(X, y)              # learn from two years of examples

for temp in [15, 25, 35]:
    guess = model.predict(pd.DataFrame({"max_temp": [temp]}))[0]
    print(f"At {temp}°C, expect about {guess:.0f} iced drinks")

plt.scatter(days["max_temp"], y, s=8, alpha=0.5, label="real days")
line = X.sort_values("max_temp")
plt.plot(line["max_temp"], model.predict(line), color="red", label="the model's line")
plt.xlabel("Maximum temperature (°C)")
plt.ylabel("Iced drinks sold")
plt.legend()
plt.savefig("first_model.png", dpi=120, bbox_inches="tight")
print("Saved first_model.png")
