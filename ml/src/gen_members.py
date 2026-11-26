"""Make loyalty_members.csv for the ML course."""
import sys, json
import numpy as np, pandas as pd
P = dict(seed=10, yseed=4, k=1.0, noise=1.0, wv=1.2, wd=1.12, wdist=0.38, wapp=0.2, wm=0.05, ws=-0.05)
P.update(json.loads(sys.argv[1]) if len(sys.argv) > 1 else {})
rng = np.random.default_rng(P["seed"])
groups = [("reg", 434, 27.1, 5.0, 9.5, 2.0, 4.5), ("treat", 422, 8.2, 3.0, 22.0, 4.5, 14.2), ("drift", 344, 2.6, 1.6, 11.5, 3.5, 57.5)]
rows = []
for name, n, v, vsd, s, ssd, d in groups:
    visits = np.clip(np.round(rng.normal(v, vsd, n)), 0, 45)
    spend = np.clip(np.round(rng.normal(s, ssd, n), 2), 4.5, 48)
    if name == "drift":
        days = np.clip(np.round(rng.normal(d, 18, n)), 25, 90)
    else:
        days = np.clip(np.round(rng.gamma(2.0, d / 2, n)), 0, 60)
    months = rng.integers(1, 61, n)
    dist = np.round(np.clip(rng.gamma(1.6, 2.2, n), 0.1, 25), 1)
    app = (rng.random(n) < {"reg": 0.7, "treat": 0.5, "drift": 0.35}[name]).astype(int)
    rows.append(pd.DataFrame({"months_as_member": months, "visits_last_90_days": visits.astype(int), "avg_spend": spend,
                              "days_since_last_visit": days.astype(int), "distance_km": dist, "uses_app": app}))
df = pd.concat(rows, ignore_index=True).sample(frac=1, random_state=P["seed"]).reset_index(drop=True)
z = lambda c: (df[c] - df[c].mean()) / df[c].std()
score = P["k"] * (P["wv"] * z("visits_last_90_days") - P["wd"] * z("days_since_last_visit") - P["wdist"] * z("distance_km")
                  + P["wapp"] * z("uses_app") + P["wm"] * z("months_as_member") + P["ws"] * z("avg_spend"))
score = score + (np.random.default_rng(P["yseed"]) if P["yseed"] else rng).logistic(0, P["noise"], len(df))
back = np.zeros(len(df), int); back[np.argsort(-score.values)[:544]] = 1
df.insert(0, "member_id", [f"M{1001 + i}" for i in range(len(df))])
df["came_back_next_month"] = back
df.to_csv(sys.argv[2] if len(sys.argv) > 2 else "data/loyalty_members.csv", index=False)
