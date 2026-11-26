"""Predict customers with linear regression, and see what it learned."""
import pandas as pd
from sklearn.linear_model import LinearRegression
from prepare import features, load_days, split_by_year

X_train, X_test, y_train, y_test = split_by_year(load_days())
model = LinearRegression().fit(X_train, y_train)

print(f"Starting point: {model.intercept_:.0f} customers")
for name, value in sorted(zip(X_train.columns, model.coef_), key=lambda p: p[1]):
    print(f"{name:26} {value:+7.1f}")

tomorrow = pd.DataFrame([{"max_temp": 28, "rain_mm": 0, "public_holiday": 0, "school_holidays": 0, "day_of_week": "Saturday"}])
X_new = features(tomorrow).reindex(columns=X_train.columns, fill_value=0)
print(f"\nA dry 28°C Saturday: about {model.predict(X_new)[0]:.0f} customers")
