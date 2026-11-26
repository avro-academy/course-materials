"""Loads the café's daily data and turns it into features (X) and the answer to learn (y)."""
import pandas as pd

FEATURES = ["max_temp", "rain_mm", "public_holiday", "school_holidays", "day_of_week"]


def load_days():
    days = pd.read_csv("data/daily_sales.csv", parse_dates=["date"])
    days["max_temp"] = days["max_temp"].fillna(days["max_temp"].median())  # fill the few missing temperatures
    return days


def features(days):
    # computers need numbers: one column per day of the week, 1 or 0 ("one-hot encoding")
    return pd.get_dummies(days[FEATURES], columns=["day_of_week"], dtype=int)


def split_by_year(days):
    """Learn from 2024, test on 2025 — like using the past to predict the future."""
    X, y = features(days), days["customers"]
    train, test = days["date"].dt.year == 2024, days["date"].dt.year == 2025
    return X[train], X[test], y[train], y[test]
