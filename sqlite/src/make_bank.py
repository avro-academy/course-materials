"""Build Alex's two bank CSV files for SQLite in Practice.

Every number shown in the lessons (monthly totals, category totals, weekday
totals, the rows shown, the balances) is a target here; the rest is random
with a fixed seed, so running it again gives the same files.

    python3 make_bank.py ../build/budget
"""
import calendar
import math
import csv
import datetime as dt
import random
import sys
from collections import defaultdict

rng = random.Random(20260101)
OPENING = 81240  # cents

COFFEE, TAKEAWAY = "BEAN THERE CAFE", "QUICKBITE TAKEAWAY"
FRESH, VALUE = "FRESHWAY SUPERMARKET", "VALUEMART GROCERIES"
PAY, RENT = "CORNER CAFE PAYROLL", "TRANSFER TO J SMITH RENT"
TRANSIT, PHONE = "CITYLINK TRANSIT TOPUP", "MOBILEPLUS PREPAID"
FLIX, TUNE = "STREAMFLIX.COM", "TUNEBOX MUSIC"
GYM, CHEM = "FITLIFE GYM", "CHEMCARE PHARMACY"
BMART, BOOKS, ATM = "BUDGETMART", "PAGEPLUS BOOKS", "ATM WITHDRAWAL CITY"


def c(x):
    return int(round(x * 100))


# (month, day or None, description, amount in cents, fixed position in the day or None, adjustable?)
T = []


def add(m, d, desc, amt, pos=None, adj=False):
    T.append({"m": m, "d": d, "desc": desc, "amt": c(amt), "pos": pos, "adj": adj, "fixed": d is not None})


# ---- January (40) ----
add(1, 1, PAY, 688.75, 0); add(1, 1, COFFEE, -5.00, 1)
add(1, 2, RENT, -420, 0); add(1, 2, COFFEE, -5.00, 1)
add(1, 3, FRESH, -61.29, 0)
add(1, 15, PAY, 612.40, 0); add(1, 29, PAY, 688.65, 0)
add(1, 16, RENT, -420, 0); add(1, 30, RENT, -420, 0)
add(1, 6, PHONE, -30); add(1, 9, FLIX, -12.99); add(1, 18, TUNE, -11.99); add(1, 24, GYM, -64.95)
for a in [5.00] * 4 + [4.50] * 4:
    add(1, None, COFFEE, -a)
for a in [18.20, 21.35, 17.60, 20.30]:            # 77.45
    add(1, None, TAKEAWAY, -a, adj=True)
for a in [48.10, 55.20, 61.75, 44.30, 58.90, 52.64, 49.80, 51.45]:   # 422.14
    add(1, None, rng.choice([FRESH, VALUE]), -a, adj=True)
add(1, None, CHEM, -12.40); add(1, None, BMART, -22.38); add(1, None, BOOKS, -13.95)
for _ in range(3):
    add(1, None, TRANSIT, -40)
add(1, None, ATM, -50)

# ---- February (46) ----
add(2, 10, VALUE, -59.52, 0); add(2, 10, COFFEE, -4.50, 1); add(2, 10, COFFEE, -5.00, 2); add(2, 10, COFFEE, -5.00, 3)
add(2, 12, PAY, 688.75, 0); add(2, 13, RENT, -420, 0)
add(2, 26, PAY, 1088.10, 0); add(2, 26, COFFEE, -5.00, 1); add(2, 26, TAKEAWAY, -19.30, 2)
add(2, 27, RENT, -420, 0); add(2, 27, COFFEE, -4.50, 1)
add(2, 28, FRESH, -70.54, 0)
add(2, 6, PHONE, -30); add(2, 9, FLIX, -12.99); add(2, 18, TUNE, -11.99); add(2, 24, GYM, -64.95)
for a in [5.00] * 7 + [4.50] * 5:
    add(2, None, COFFEE, -a)
for a in [16.85, 18.40, 16.37]:                   # 51.62
    add(2, None, TAKEAWAY, -a, adj=True)
for a in [41.20, 47.85, 39.60, 45.10, 43.94, 42.40]:  # 260.09
    add(2, None, rng.choice([FRESH, VALUE]), -a, adj=True)
for a in [40, 20, 20, 40, 20, 20]:
    add(2, None, TRANSIT, -a)
add(2, None, CHEM, -9.80); add(2, None, BMART, -25.75); add(2, None, BMART, -19.45)

# ---- March (48) ----
add(3, 12, PAY, 845.60, 0); add(3, 26, PAY, 867.65, 0)
add(3, 13, RENT, -420, 0); add(3, 27, RENT, -420, 0)
add(3, 6, PHONE, -30); add(3, 9, FLIX, -12.99); add(3, 18, TUNE, -11.99); add(3, 24, GYM, -64.95)
add(3, 30, TRANSIT, -40, 98); add(3, 30, COFFEE, -5.20, 99)
add(3, 31, VALUE, -32.57, 0); add(3, 31, COFFEE, -5.20, 1)
for a in [5.20] * 10 + [4.70] * 4:
    add(3, None, COFFEE, -a)
for a in [19.10, 17.95, 20.25, 17.22]:            # 74.52
    add(3, None, TAKEAWAY, -a, adj=True)
for a in [49.30, 51.85, 46.70, 53.20, 47.95, 50.40, 48.63, 47.40]:   # 395.43
    add(3, None, rng.choice([FRESH, VALUE]), -a, adj=True)
for a in [40, 40, 20]:
    add(3, None, TRANSIT, -a)
add(3, None, CHEM, -24.30); add(3, None, CHEM, -18.90)
add(3, None, BOOKS, -18.95); add(3, None, BMART, -64.99); add(3, None, BMART, -42.95)
add(3, None, BOOKS, 18.95)   # the refund, after the purchase
add(3, None, ATM, -50)

# ---- targets ----
MONTH_COUNT = {1: 40, 2: 46, 3: 48}
MONTH_IN = {1: c(1989.80), 2: c(1776.85), 3: c(1732.20)}
MONTH_OUT = {1: c(2207.54), 2: c(1717.50), 3: c(1903.74)}
WEEKDAY_OUT = {0: c(96.83), 1: c(588.40), 2: c(688.35), 3: c(249.52), 4: c(204.46), 5: c(3074.30), 6: c(926.92)}
FEB_1_TO_9 = c(278.39)
NO_EXTRA = {(1, 1), (1, 2), (2, 1), (2, 10), (2, 26), (2, 27), (2, 28), (3, 31)}

for m in (1, 2, 3):
    rows = [t for t in T if t["m"] == m]
    assert len(rows) == MONTH_COUNT[m], (m, len(rows))
    assert sum(t["amt"] for t in rows if t["amt"] > 0) == MONTH_IN[m], m
    assert sum(-t["amt"] for t in rows if t["amt"] < 0) == MONTH_OUT[m], (m, sum(-t["amt"] for t in rows if t["amt"] < 0))
assert sum(WEEKDAY_OUT.values()) == sum(MONTH_OUT.values())


def wday(m, d):  # 0 = Sunday, like strftime('%w')
    return (dt.date(2026, m, d).weekday() + 1) % 7


flex = [t for t in T if not t["fixed"]]
for t in flex:
    days = [d for d in range(1, calendar.monthrange(2026, t["m"])[1] + 1) if (t["m"], d) not in NO_EXTRA]
    t["d"] = rng.choice(days)
    t["days"] = days
refund = next(t for t in T if t["desc"] == BOOKS and t["amt"] > 0)
purchase = next(t for t in T if t["desc"] == BOOKS and t["m"] == 3 and t["amt"] < 0)


def ordered():
    key = {}
    for t in T:
        p = t["pos"]
        if p is None:
            p = 50 + t.setdefault("r", rng.random())
        key[id(t)] = (t["m"], t["d"], p)
    return sorted(T, key=lambda t: key[id(t)])


def cost():
    wd = defaultdict(int)
    feb = 0
    seen = defaultdict(int)
    per_day = defaultdict(int)
    for t in T:
        if t["amt"] < 0:
            wd[wday(t["m"], t["d"])] += -t["amt"]
            if t["m"] == 2 and t["d"] <= 9:
                feb += -t["amt"]
        seen[(t["m"], t["d"], t["desc"], t["amt"])] += 1
        per_day[(t["m"], t["d"])] += 1
    s = sum(abs(wd[k] - v) for k, v in WEEKDAY_OUT.items()) + abs(feb - FEB_1_TO_9) * 2
    s += 500 * sum(n - 1 for k, n in seen.items() if n > 1 and k != (2, 10, COFFEE, -500))
    s += 300 * sum(n - 4 for n in per_day.values() if n > 4)
    s += 2000 * (refund["d"] <= purchase["d"])
    bal = OPENING
    for t in ordered():
        bal += t["amt"]
        if bal < 2000:   # keep at least $20
            s += (2000 - bal) // 10 + 50
    return s


cur = cost()
adj = defaultdict(list)
for t in T:
    if t["adj"]:
        adj[(t["m"], t["desc"] == TAKEAWAY)].append(t)
step = 0
while cur > 0:
    step += 1
    if step > 600000:
        raise SystemExit(f"could not fit: {cur}")
    temp = max(0.3, 150 * (1 - step / 250000))
    if rng.random() < 0.6:
        t = rng.choice(flex)
        old = t["d"]
        t["d"] = rng.choice(t["days"])
        new = cost()
        if new <= cur or rng.random() < math.exp((cur - new) / temp):
            cur = new
        else:
            t["d"] = old
    else:
        group = rng.choice(list(adj.values()))
        a, b = rng.sample(group, 2)
        k = rng.choice([1, 2, 5, 10, 25, 50, 100])
        lo = 1200 if a["desc"] == TAKEAWAY else 3000
        hi = 2800 if a["desc"] == TAKEAWAY else 7000
        if not (lo <= -(a["amt"] - k) <= hi and lo <= -(b["amt"] + k) <= hi):
            continue
        a["amt"] -= k; b["amt"] += k
        new = cost()
        if new <= cur or rng.random() < math.exp((cur - new) / temp):
            cur = new
        else:
            a["amt"] += k; b["amt"] -= k


def money(v, commas):
    s = f"{v / 100:.2f}"
    if commas and abs(v) >= 100000:
        s = f"{v / 100:,.2f}"
    return s


def write(path, months):
    rows = []
    bal = OPENING
    for t in ordered():
        bal += t["amt"]
        if t["m"] in months:
            rows.append((t, bal))
    rows.reverse()  # newest first, like the bank
    with open(path, "w", newline="") as f:
        w = csv.writer(f, lineterminator="\r\n")
        w.writerow(["Date", "Description", "Amount", "Balance"])
        for t, b in rows:
            w.writerow([f"{t['d']:02d}/{t['m']:02d}/2026", t["desc"], money(t["amt"], True), money(b, True)])


out = sys.argv[1]
write(f"{out}/everyday-2026-01-to-02.csv", (1, 2))
write(f"{out}/everyday-2026-02-to-03.csv", (2, 3))
print("fitted in", step, "steps")
