"""Split the data: learn from one part, test on a part the model has never seen."""
from sklearn.model_selection import train_test_split
from prepare import features, load_days, split_by_year

days = load_days()
X_train, X_test, y_train, y_test = split_by_year(days)
print(f"By year:  learn from {len(X_train)} days (2024), test on {len(X_test)} days (2025)")

X_train, X_test, y_train, y_test = train_test_split(features(days), days["customers"], test_size=0.2, random_state=1)
print(f"Random:   learn from {len(X_train)} days, test on {len(X_test)} days")
