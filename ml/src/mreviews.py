import sys, warnings; warnings.filterwarnings("ignore")
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
reviews = pd.read_csv(sys.argv[1] if len(sys.argv) > 1 else "data/reviews.csv")
reviews["happy"] = (reviews["stars"] >= 4).astype(int)
X_train, X_test, y_train, y_test = train_test_split(reviews["text"], reviews["happy"], test_size=0.25, random_state=1)
m = make_pipeline(TfidfVectorizer(ngram_range=(1, 2)), LogisticRegression()).fit(X_train, y_train)
print(f"acc {accuracy_score(y_test, m.predict(X_test)):.0%} (93)  happy share {reviews.happy.mean():.0%}")
w = m.named_steps["tfidfvectorizer"].get_feature_names_out(); c = m.named_steps["logisticregression"].coef_[0]
r = sorted(zip(c, w)); print("U:", ", ".join(x for _, x in r[:8]), "(was, but that, that, cold, unfriendly, unfriendly service, won, won be)")
print("H:", ", ".join(x for _, x in r[-8:][::-1]), "(lovely, was excellent, excellent, with, is, loved, no complaints, no)")
for t, e in [("Lovely staff and the best coffee around!", 77), ("Cold toastie and we waited forever.", 52), ("Not bad at all.", 67), ("The coffee was not good.", 50)]:
    print(f"{m.predict_proba([t])[0,1]:.0%} ({e})", end="  ")
print()
