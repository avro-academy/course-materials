"""Happy or unhappy? Teach a model to read customer reviews."""
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline

reviews = pd.read_csv("data/reviews.csv")
reviews["happy"] = (reviews["stars"] >= 4).astype(int)
X_train, X_test, y_train, y_test = train_test_split(reviews["text"], reviews["happy"], test_size=0.25, random_state=1)

# turn each review into numbers (which words and word pairs appear), then learn
model = make_pipeline(TfidfVectorizer(ngram_range=(1, 2)), LogisticRegression())
model.fit(X_train, y_train)
print(f"Right on {accuracy_score(y_test, model.predict(X_test)):.0%} of reviews it hasn't seen")

words = model.named_steps["tfidfvectorizer"].get_feature_names_out()
weights = model.named_steps["logisticregression"].coef_[0]
ranked = sorted(zip(weights, words))
print("Most unhappy words:", ", ".join(w for _, w in ranked[:8]))
print("Most happy words:  ", ", ".join(w for _, w in ranked[-8:][::-1]))

print()
for text in ["Lovely staff and the best coffee around!", "Cold toastie and we waited forever.",
             "Not bad at all.", "The coffee was not good."]:
    chance = model.predict_proba([text])[0, 1]
    print(f"{chance:4.0%} happy  {text}")
