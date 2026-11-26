"""Module 6 project: weekly roster hours report. Run from the starter folder: python scripts/roster_report.py"""
import pandas as pd
from pathlib import Path

RATES = {"Saturday": 1.25, "Sunday": 1.5}
BASE = 25

def roster_report(folder):
    files = sorted(Path(folder).glob("roster_week_*.csv"))
    roster = pd.concat([pd.read_csv(f) for f in files], ignore_index=True)
    roster["weekend"] = roster["day"].isin(["Saturday", "Sunday"])
    roster["pay"] = roster["hours"] * BASE * roster["day"].map(RATES).fillna(1)
    report = roster.groupby("name").agg(
        shifts=("day", "count"),
        hours=("hours", "sum"),
        weekend_hours=("hours", lambda h: h[roster.loc[h.index, "weekend"]].sum()),
        est_pay=("pay", "sum"),
    ).sort_values("hours", ascending=False)
    return report.round(2), len(files)

report, weeks = roster_report("data/rosters")
print(f"Roster report: {weeks} weeks")
print(report)
report.to_csv("roster_report.csv")
