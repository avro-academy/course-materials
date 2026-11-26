"""Train the final model on all the data and save it to a file."""
import joblib
import pandas as pd
from sklearn.compose import make_column_transformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder

FEATURES = ["max_temp", "rain_mm", "public_holiday", "school_holidays", "day_of_week"]
days = pd.read_csv("data/daily_sales.csv")

model = make_pipeline(
    make_column_transformer((SimpleImputer(strategy="median"), ["max_temp"]),
                            (OneHotEncoder(handle_unknown="ignore"), ["day_of_week"]), remainder="passthrough"),
    RandomForestRegressor(n_estimators=300, min_samples_leaf=3, random_state=1))
model.fit(days[FEATURES], days["customers"])

joblib.dump(model, "customers_model.joblib")
print(f"Trained on {len(days)} days and saved customers_model.joblib")
