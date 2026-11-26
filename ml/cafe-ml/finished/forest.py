"""Decision trees and random forests: models that learn rules, and can follow curves."""
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.tree import DecisionTreeRegressor, export_text
from prepare import load_days, split_by_year

X_train, X_test, y_train, y_test = split_by_year(load_days())

small = DecisionTreeRegressor(max_depth=2, random_state=1).fit(X_train, y_train)
print(export_text(small, feature_names=list(X_train.columns), decimals=1))

def mae(model, X, y):
    return mean_absolute_error(y, model.predict(X))

deep = DecisionTreeRegressor(random_state=1).fit(X_train, y_train)
print(f"Deep tree:      MAE {mae(deep, X_train, y_train):5.1f} on 2024 (learned)   {mae(deep, X_test, y_test):5.1f} on 2025 (new)")
forest = RandomForestRegressor(n_estimators=300, min_samples_leaf=3, random_state=1).fit(X_train, y_train)
print(f"Random forest:  MAE {mae(forest, X_train, y_train):5.1f} on 2024 (learned)   {mae(forest, X_test, y_test):5.1f} on 2025 (new)")

print("\nWhat mattered most to the forest:")
for name, importance in sorted(zip(X_train.columns, forest.feature_importances_), key=lambda p: -p[1])[:5]:
    print(f"  {name:26} {importance:.0%}")
