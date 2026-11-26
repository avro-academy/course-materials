"""Beyond accuracy: which mistakes does the model make, and which matter?"""
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

members = pd.read_csv("data/loyalty_members.csv")
X = members.drop(columns=["member_id", "came_back_next_month"])
y = members["came_back_next_month"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=1, stratify=y)
model = make_pipeline(StandardScaler(), LogisticRegression()).fit(X_train, y_train)

print("Confusion matrix (rows = what really happened, columns = predicted)")
print(pd.DataFrame(confusion_matrix(y_test, model.predict(X_test)),
                   index=["really didn't", "really came back"], columns=["predicted didn't", "predicted came back"]))
print()
print(classification_report(y_test, model.predict(X_test), target_names=["didn't come back", "came back"]))

# The café wants to send a "we miss you" voucher to members who probably won't come back.
chance_back = model.predict_proba(X_test)[:, 1]
for cutoff in [0.5, 0.3, 0.7]:
    send = chance_back < cutoff
    caught = ((y_test == 0) & send).sum()
    print(f"Voucher if chance of coming back < {cutoff:.0%}: send {send.sum():3} vouchers, "
          f"reach {caught} of {(y_test == 0).sum()} who wouldn't have come back, {send.sum() - caught} wasted")
