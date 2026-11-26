"""Look at the features the models will learn from."""
from prepare import features, load_days

days = load_days()
X, y = features(days), days["customers"]
print(list(X.columns))
print(X.head(3).T)          # .T turns the table sideways, so every column fits
print(y.head(3))
