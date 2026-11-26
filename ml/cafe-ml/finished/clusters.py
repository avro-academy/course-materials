"""Find groups of similar members, without telling the computer what the groups are."""
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

members = pd.read_csv("data/loyalty_members.csv")
habits = members[["visits_last_90_days", "avg_spend", "days_since_last_visit"]]

scaled = StandardScaler().fit_transform(habits)                 # put all three on the same scale
members["group"] = KMeans(n_clusters=3, n_init=10, random_state=1).fit_predict(scaled)

summary = members.groupby("group")[list(habits.columns)].mean().round(1)
summary["members"] = members["group"].value_counts()
print(summary)

plt.scatter(members["visits_last_90_days"], members["avg_spend"], c=members["group"], s=10, cmap="viridis")
plt.xlabel("Visits in the last 90 days")
plt.ylabel("Average spend ($)")
plt.title("Three groups the model found")
plt.savefig("clusters.png", dpi=120, bbox_inches="tight")
print("Saved clusters.png")
