"""How good are the predictions? Compare with a simple guess, on days the model hasn't seen."""
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score, root_mean_squared_error
from prepare import load_days, split_by_year

days = load_days()
X_train, X_test, y_train, y_test = split_by_year(days)

baseline = [y_train.mean()] * len(y_test)       # always guess the 2024 average
model = LinearRegression().fit(X_train, y_train)
predicted = model.predict(X_test)

for name, guess in [("Always guess the average", baseline), ("Linear regression", predicted)]:
    print(f"{name:26} MAE {mean_absolute_error(y_test, guess):5.1f}   "
          f"RMSE {root_mean_squared_error(y_test, guess):5.1f}   R² {r2_score(y_test, guess):5.2f}")

dates = days[days["date"].dt.year == 2025]["date"]
plt.figure(figsize=(12, 4))
plt.plot(dates, y_test, linewidth=0.8, label="real customers")
plt.plot(dates, predicted, linewidth=0.8, label="predicted")
plt.title("2025: real and predicted customers")
plt.legend()
plt.savefig("evaluate.png", dpi=110, bbox_inches="tight")
print("Saved evaluate.png")
