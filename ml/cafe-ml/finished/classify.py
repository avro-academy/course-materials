"""Will a loyalty member come back next month? A classification model."""
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

members = pd.read_csv("data/loyalty_members.csv")
X = members.drop(columns=["member_id", "came_back_next_month"])
y = members["came_back_next_month"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=1, stratify=y)

model = make_pipeline(StandardScaler(), LogisticRegression())   # scale the numbers, then learn
model.fit(X_train, y_train)

print(f"Came back in the training data: {y_train.mean():.0%}")
print(f"Always guess 'won't come back': {accuracy_score(y_test, [0] * len(y_test)):.0%} right")
print(f"The model:                      {accuracy_score(y_test, model.predict(X_test)):.0%} right")

print("\nWhat pushes towards coming back (+) or not (−):")
coefs = model.named_steps["logisticregression"].coef_[0]
for name, value in sorted(zip(X.columns, coefs), key=lambda p: -p[1]):
    print(f"  {name:24} {value:+.2f}")
