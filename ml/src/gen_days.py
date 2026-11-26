"""Make daily_sales.csv for the ML course."""
import sys, json
import numpy as np, pandas as pd

P = dict(seed=1, tmean=20.2, tamp=5.5, tsd=3.3, heat_p=0.05, heat_add=9.0, rain_p=0.33, rain_mean=8.0,
         base24=226.0, growth=15.0, peak=20.0, curve=0.8, hot=35.0, hotdrop=135.0, cold=16.5, colddrop=10.0,
         rain_k=3.4, ph=40.0, sh=13.0, noise=11.0, sh_k=1.0, warm=26.0, warmk=2.0)
P.update(json.loads(sys.argv[1]) if len(sys.argv) > 1 else {})
rng = np.random.default_rng(P["seed"])
dates = pd.date_range("2024-01-01", "2025-12-31")
dates = dates[~((dates.month == 12) & (dates.day == 25))]
n = len(dates)
doy = dates.day_of_year.values
season = np.cos(2 * np.pi * (doy - 20) / 365.25)
temp = P["tmean"] + P["tamp"] * season + rng.normal(0, P["tsd"], n)
heat = (rng.random(n) < P["heat_p"] * np.clip(season, 0, 1) * 2)
temp = temp + heat * rng.uniform(0.6, 1.3, n) * P["heat_add"]
temp = np.round(temp, 1)
rain = np.where(rng.random(n) < P["rain_p"], np.round(rng.exponential(P["rain_mean"], n) + 0.2, 1), 0.0)

ph_dates = {"2024-01-01","2024-01-26","2024-03-29","2024-04-01","2024-04-25","2024-06-10","2024-10-07","2024-12-26",
            "2025-01-01","2025-01-27","2025-04-18","2025-04-21","2025-04-25","2025-06-09","2025-10-06","2025-12-26"}
ph = np.array([d.strftime("%Y-%m-%d") in ph_dates for d in dates]).astype(int)
sh_ranges = [("2024-01-02","2024-01-31"),("2024-04-13","2024-04-28"),("2024-07-06","2024-07-21"),("2024-09-28","2024-10-13"),
             ("2024-12-20","2025-01-31"),("2025-04-12","2025-04-27"),("2025-07-05","2025-07-20"),("2025-09-27","2025-10-12"),
             ("2025-12-19","2025-12-31")]
sh = np.zeros(n, int)
for a, b in sh_ranges:
    sh[(dates >= a) & (dates <= b)] = 1
sh[:3] = 0  # matches the lesson's first rows
dow = dates.day_name()
deff = {"Monday": -46, "Tuesday": -28, "Wednesday": -21, "Thursday": -17, "Friday": 5, "Saturday": 60, "Sunday": 43}
t = (dates - dates[0]).days.values / 365.0
c = (P["base24"] + P["growth"] * t + np.array([deff[d] for d in dow])
     - P["curve"] * (temp - P["peak"]) ** 2 * 0.1
     - np.where(temp > P["hot"], P["hotdrop"] * np.minimum(1, (temp - P["hot"]) / 2.5), 0)
     - np.where(temp > P["warm"], P["warmk"] * (temp - P["warm"]), 0)
     - np.where(temp < P["cold"], P["colddrop"] * (P["cold"] - temp), 0)
     - P["rain_k"] * rain + P["ph"] * ph + P["sh"] * sh * P["sh_k"])
cust = np.maximum(np.round(c + rng.normal(0, P["noise"], n)), 38).astype(int)  # never fewer than 38 customers
g = np.clip(0.1 * (temp - 8.5) ** 2 * (temp > 8.5), 0, None) * (0.6 + 0.4 * cust / 220)
iced = np.maximum(0, np.round(g + rng.normal(0, 4.5, n))).astype(int)
df = pd.DataFrame({"date": dates.strftime("%Y-%m-%d"), "day_of_week": dow, "max_temp": temp, "rain_mm": rain,
                   "public_holiday": ph, "school_holidays": sh, "customers": cust, "iced_drinks": iced})
# fixed first rows from the lesson
df.loc[0, ["max_temp","rain_mm","customers","iced_drinks"]] = [20.6, 0.0, 218, 8]
df.loc[1, ["max_temp","rain_mm","customers","iced_drinks"]] = [np.nan, 0.0, 175, 35]
df.loc[2, ["max_temp","rain_mm","customers","iced_drinks"]] = [21.4, 0.0, 216, 16]
miss = rng.choice(np.arange(10, n), 6, replace=False)
df.loc[miss, "max_temp"] = np.nan
# nudge one temperature so the median is exactly 20.2, as in the lesson
while round(df["max_temp"].median(), 2) != 20.2:
    hi = df["max_temp"].dropna().sort_values().iloc[len(df["max_temp"].dropna()) // 2]
    k = df.index[df["max_temp"] == hi][-1]
    df.loc[k, "max_temp"] = round(hi - 0.1, 1)
df["customers"] = df["customers"].astype(int); df["iced_drinks"] = df["iced_drinks"].astype(int)
df.to_csv(sys.argv[2] if len(sys.argv) > 2 else "data/daily_sales.csv", index=False)
