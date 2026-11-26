"""Fairer scores with cross-validation, and a pipeline that does all the preparation itself."""
from sklearn.compose import make_column_transformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import KFold, cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder
import pandas as pd

days = pd.read_csv("data/daily_sales.csv")        # raw data: missing temperatures, day names as text
X = days[["max_temp", "rain_mm", "public_holiday", "school_holidays", "day_of_week"]]
y = days["customers"]

prepare = make_column_transformer(
    (SimpleImputer(strategy="median"), ["max_temp"]),       # fill missing temperatures
    (OneHotEncoder(), ["day_of_week"]),                      # day names → 1/0 columns
    remainder="passthrough")

folds = KFold(n_splits=5, shuffle=True, random_state=1)
for name, model in [("Linear regression", LinearRegression()),
                    ("Random forest", RandomForestRegressor(n_estimators=200, min_samples_leaf=3, random_state=1))]:
    pipeline = make_pipeline(prepare, model)
    scores = -cross_val_score(pipeline, X, y, cv=folds, scoring="neg_mean_absolute_error")
    print(f"{name:18} MAE in each of 5 tests: {', '.join(f'{s:.1f}' for s in scores)}   average {scores.mean():.1f}")
