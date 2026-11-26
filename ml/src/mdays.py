import sys, warnings; warnings.filterwarnings("ignore")
import numpy as np, pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor, export_text
from sklearn.metrics import mean_absolute_error as MAE, root_mean_squared_error as RMSE, r2_score as R2
from sklearn.compose import make_column_transformer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import KFold, cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder
f = sys.argv[1] if len(sys.argv) > 1 else "data/daily_sales.csv"
full = "full" in sys.argv
raw = pd.read_csv(f, parse_dates=["date"])
d = raw.dropna(); m = LinearRegression().fit(d[["max_temp"]], d["iced_drinks"])
print("iced", [round(m.predict(pd.DataFrame({"max_temp":[t]}))[0]) for t in (15,25,35)], "(6 29 51)")
order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
print("dow", list(raw.groupby("day_of_week")["customers"].mean().reindex(order).round().astype(int)), "(177 195 201 205 232 283 265)")
print("dry/rain", round(raw[raw.rain_mm==0].customers.mean()), round(raw[raw.rain_mm>0].customers.mean()), "(229 198)", "median", raw.max_temp.median(), "(20.2)")
days = raw.copy(); days["max_temp"] = days["max_temp"].fillna(days["max_temp"].median())
F = ["max_temp","rain_mm","public_holiday","school_holidays","day_of_week"]
X = pd.get_dummies(days[F], columns=["day_of_week"], dtype=int); y = days.customers
tr, te = days.date.dt.year==2024, days.date.dt.year==2025
Xtr, Xte, ytr, yte = X[tr], X[te], y[tr], y[te]
lr = LinearRegression().fit(Xtr, ytr)
print("lr int %.0f (206)" % lr.intercept_, " ".join(f"{n.replace('day_of_week_','')[:3]}:{v:+.1f}" for n, v in zip(X.columns, lr.coef_)))
print("   (temp+0.5 rain-3.4 ph+40.4 sh+10.4 Fri+2.6 Mon-44 Sat+59.1 Sun+43.9 Thu-17.4 Tue-26.8 Wed-17.4)")
tom = pd.DataFrame([{"max_temp":28,"rain_mm":0,"public_holiday":0,"school_holidays":0,"day_of_week":"Saturday"}])
print("sat28 %.0f (279)" % lr.predict(pd.get_dummies(tom[F], columns=["day_of_week"], dtype=int).reindex(columns=X.columns, fill_value=0))[0])
b = [ytr.mean()]*len(yte); p = lr.predict(Xte)
print("base MAE %.1f RMSE %.1f R2 %.2f (38.6 50.6 -0.12)" % (MAE(yte,b), RMSE(yte,b), R2(yte,b)))
print("lr   MAE %.1f RMSE %.1f R2 %.2f (25.0 30.2 0.60)" % (MAE(yte,p), RMSE(yte,p), R2(yte,p)))
if full:
    sm = DecisionTreeRegressor(max_depth=2, random_state=1).fit(Xtr, ytr); print(export_text(sm, feature_names=list(X.columns), decimals=1))
    dp = DecisionTreeRegressor(random_state=1).fit(Xtr, ytr)
    print("deep %.1f %.1f (0.8 22.8)" % (MAE(ytr, dp.predict(Xtr)), MAE(yte, dp.predict(Xte))))
    rf = RandomForestRegressor(n_estimators=300, min_samples_leaf=3, random_state=1, n_jobs=4).fit(Xtr, ytr)
    print("rf %.1f %.1f (10.9 20.3)" % (MAE(ytr, rf.predict(Xtr)), MAE(yte, rf.predict(Xte))))
    print(" ", [(n.replace('day_of_week_',''), f"{v:.0%}") for n, v in sorted(zip(X.columns, rf.feature_importances_), key=lambda p:-p[1])[:5]], "(Sat29 Sun24 temp22 rain15 Fri6)")
    prep = make_column_transformer((SimpleImputer(strategy="median"), ["max_temp"]), (OneHotEncoder(), ["day_of_week"]), remainder="passthrough")
    folds = KFold(n_splits=5, shuffle=True, random_state=1)
    for name, mod in [("LR", LinearRegression()), ("RF", RandomForestRegressor(n_estimators=200, min_samples_leaf=3, random_state=1, n_jobs=4))]:
        s = -cross_val_score(make_pipeline(prep, mod), raw[F], raw.customers, cv=folds, scoring="neg_mean_absolute_error")
        print(name, [round(v,1) for v in s], round(s.mean(),1))
    print("   (LR 21.0 19.9 20.0 21.1 19.3 = 20.3; RF 16.3 15.6 16.6 17.7 16.1 = 16.5)")
    fin = make_pipeline(make_column_transformer((SimpleImputer(strategy="median"), ["max_temp"]), (OneHotEncoder(handle_unknown="ignore"), ["day_of_week"]), remainder="passthrough"),
                        RandomForestRegressor(n_estimators=300, min_samples_leaf=3, random_state=1, n_jobs=4)).fit(raw[F], raw.customers)
    q = pd.DataFrame([{"max_temp":31,"rain_mm":0,"public_holiday":0,"school_holidays":0,"day_of_week":"Saturday"},
                      {"max_temp":14,"rain_mm":12,"public_holiday":1,"school_holidays":0,"day_of_week":"Monday"}])
    print("predict", [round(v) for v in fin.predict(q)], "(250 127)")
