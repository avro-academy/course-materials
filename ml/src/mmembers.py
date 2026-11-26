import sys, warnings; warnings.filterwarnings("ignore")
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
members = pd.read_csv(sys.argv[1] if len(sys.argv) > 1 else "data/loyalty_members.csv")
X = members.drop(columns=["member_id", "came_back_next_month"]); y = members["came_back_next_month"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=1, stratify=y)
m = make_pipeline(StandardScaler(), LogisticRegression()).fit(X_train, y_train)
print(f"back {y_train.mean():.0%} base {accuracy_score(y_test,[0]*len(y_test)):.0%} model {accuracy_score(y_test, m.predict(X_test)):.0%} (45 55 81)")
print(" ".join(f"{n[:8]}{v:+.2f}" for n, v in sorted(zip(X.columns, m.named_steps['logisticregression'].coef_[0]), key=lambda p:-p[1])), "(visits+1.20 app+0.13 months+0.05 spend-0.05 dist-0.38 days-1.12)")
print(confusion_matrix(y_test, m.predict(X_test)).tolist(), "([[136,28],[30,106]])")
if "full" in sys.argv: print(classification_report(y_test, m.predict(X_test), target_names=["didn't come back", "came back"]))
ch = m.predict_proba(X_test)[:, 1]
for c in [0.5, 0.3, 0.7]:
    s = ch < c; caught = ((y_test == 0) & s).sum(); print(c, s.sum(), caught, s.sum() - caught, end=" | ")
print("(166 136 30 | 112 103 9 | 195 149 46)")
h = members[["visits_last_90_days", "avg_spend", "days_since_last_visit"]]
members["group"] = KMeans(n_clusters=3, n_init=10, random_state=1).fit_predict(StandardScaler().fit_transform(h))
sm = members.groupby("group")[list(h.columns)].mean().round(1); sm["members"] = members["group"].value_counts()
print(sm.to_string() if "full" in sys.argv else sm.values.tolist(), "(8.2 22.0 14.2 422 / 27.1 9.5 4.5 434 / 2.6 11.5 57.5 344)")
