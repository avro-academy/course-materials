"""Build cafe.sql: the Corner Café database for PostgreSQL Foundations.

Every number shown in the lessons (counts, totals, best days, best customers,
the first and last orders) is built in here as a target; the rest is random
with a fixed seed, so running this again gives exactly the same file.

    python3 make_cafe.py ../build/cafe-sql/cafe.sql
"""
import math
import random
import sys
from collections import Counter, defaultdict

rng = random.Random(20260301)

CATEGORIES = ["Coffee", "Tea", "Drinks", "Food"]
# name, category, price (dollars), vegetarian, available, sold in March
MENU = [
    ("Flat white", 1, "4.80", True, True, 513),
    ("Latte", 1, "4.80", True, True, 474),
    ("Cappuccino", 1, "4.80", True, True, 312),
    ("Long black", 1, "4.20", True, True, 194),
    ("Chai latte", 2, "5.20", True, True, 155),
    ("English breakfast tea", 2, "4.00", True, True, 87),
    ("Hot chocolate", 3, "5.00", True, True, 137),
    ("Iced coffee", 3, "6.50", True, True, 86),
    ("Orange juice", 3, "5.50", True, True, 110),
    ("Banana bread", 4, "5.50", True, True, 256),
    ("Ham and cheese toastie", 4, "9.50", False, True, 216),
    ("Veggie wrap", 4, "11.00", True, True, 147),
    ("Muffin", 4, "4.50", True, True, 194),
    ("Lemon slice", 4, "4.50", True, True, 108),
    ("Pumpkin soup", 4, "9.00", True, False, 0),
]
PRICE = {i + 1: int(round(float(m[2]) * 10)) for i, m in enumerate(MENU)}  # in 10c

STAFF = [  # first, last, role, rate, started, email
    ("Sam", "Lee", "Manager", "38.50", "2021-02-01"),
    ("Priya", "Shah", "Barista", "29.10", "2023-06-12"),
    ("Jordan", "Nguyen", "Barista", "28.40", "2024-01-15"),
    ("Mia", "Rossi", "Cashier", "26.80", "2025-03-03"),
    ("Ali", "Hassan", "Cashier", "25.90", "2025-11-20"),
    ("Chen", "Wu", "Kitchen", "31.20", "2022-08-08"),
]
STAFF_ORDERS = {1: 265, 2: 438, 3: 321, 4: 305, 5: 163}

CUSTOMERS = [  # name, has email, joined
    "Olivia Smith", "Liam Kim", "Ava Brown", "Noah Jones", "Ethan Wilson",
    "Aisha Tran", "Jack Taylor", "Grace Patel", "Amelia Chen", "Oscar Wright",
    "Kai Martin", "Ben Walker", "Isla Thompson", "Arjun White", "Zoe Harris",
    "Ruby Scott", "Hana Nakamura", "Tom Evans", "Sophie Green", "Mason Hall",
    "Ella Robinson", "Finn Murphy", "Lily Wood", "Max King", "Chloe Clarke",
]
NO_EMAIL = {"Aisha Tran", "Ben Walker"}
JOINED = {"Max King": "2026-01-20", "Chloe Clarke": "2026-02-15"}
CID = {n: i + 1 for i, n in enumerate(CUSTOMERS)}
# loyalty orders per customer (502 in all) and exact spend in 10c for the top 5
CUST_ORDERS = {"Liam Kim": 55, "Aisha Tran": 40, "Jack Taylor": 38,
               "Olivia Smith": 37, "Kai Martin": 36, "Ethan Wilson": 13,
               "Max King": 0, "Chloe Clarke": 0}
CUST_SPEND = {"Liam Kim": 6734, "Aisha Tran": 4520, "Jack Taylor": 4369,
              "Olivia Smith": 4195, "Kai Martin": 4060}
CUST_MAX_OTHER = 4059

# March 2026: the 1st is a Sunday
DAY_ORDERS = {
    1: 66, 8: 67, 15: 58, 22: 57, 29: 55,           # Sundays 303
    7: 54, 14: 55, 21: 54, 28: 55,                  # Saturdays 218
    2: 39, 9: 46, 16: 47, 23: 46, 30: 46,           # Mondays 224
    3: 39, 10: 44, 17: 43, 24: 44, 31: 44,          # Tuesdays 214
    4: 46, 11: 46, 18: 47, 25: 46,                  # Wednesdays 185
    5: 45, 12: 44, 19: 45, 26: 45,                  # Thursdays 179
    6: 42, 13: 43, 20: 42, 27: 42,                  # Fridays 169
}
HOUR_ORDERS = {7: 202, 8: 310, 9: 254, 10: 178, 11: 128, 12: 187, 13: 149, 14: 84}
# exact takings (10c) for some days; every other day strictly between
DAY_TAKINGS = {1: 7611, 8: 6541, 22: 6134, 2: 3985, 3: 4287, 6: 3931}
DAY_MIN, DAY_MAX = 3932, 6133
TOTAL_LINES = 2454
CARD, CASH = 1204, 288
LOYALTY = 502

assert sum(DAY_ORDERS.values()) == 1492 == sum(HOUR_ORDERS.values())
assert sum(STAFF_ORDERS.values()) == 1492 == CARD + CASH


def build_orders():
    days = [d for d in range(1, 32) for _ in range(DAY_ORDERS[d])]
    hours = [h for h, n in HOUR_ORDERS.items() for _ in range(n)]
    rng.shuffle(hours)
    orders = [{"day": d, "hour": h} for d, h in zip(days, hours)]

    def count(day, hour):
        return sum(1 for o in orders if o["day"] == day and o["hour"] == hour)

    def move(day, hour, want):
        # swap hours with orders on other days until `day` has `want` orders in `hour`
        while count(day, hour) != want:
            have = count(day, hour)
            mine = [o for o in orders if o["day"] == day and (o["hour"] == hour) == (have > want)]
            other = [o for o in orders if o["day"] not in (1, 31) and (o["hour"] == hour) != (have > want)]
            a, b = rng.choice(mine), rng.choice(other)
            a["hour"], b["hour"] = b["hour"], a["hour"]

    move(1, 7, 3)
    move(1, 8, max(count(1, 8), 3))
    move(31, 14, 1)
    move(31, 13, max(count(31, 13), 3))
    # minutes and seconds
    fixed_first = ["07:29:36", "07:34:17", "07:55:48", "08:00:06", "08:07:39"]
    fixed_last = ["13:39:24", "13:58:20", "14:01:53"]
    used = set()
    for o in orders:
        while True:
            m, s = rng.randrange(60), rng.randrange(60)
            t = f"{o['hour']:02d}:{m:02d}:{s:02d}"
            if o["day"] == 1 and o["hour"] == 8 and t <= "08:07:39":
                continue
            if o["day"] == 31 and o["hour"] == 13 and t >= "13:39:24":
                continue
            if (o["day"], t) not in used:
                break
        used.add((o["day"], t))
        o["time"] = t
    # put the fixed times in place
    d1 = sorted([o for o in orders if o["day"] == 1 and o["hour"] == 7], key=lambda o: o["time"])
    d1 += sorted([o for o in orders if o["day"] == 1 and o["hour"] == 8], key=lambda o: o["time"])[:2]
    for o, t in zip(d1, fixed_first):
        o["time"] = t
    d31 = sorted([o for o in orders if o["day"] == 31 and o["hour"] == 13], key=lambda o: o["time"])[-2:]
    d31 += [o for o in orders if o["day"] == 31 and o["hour"] == 14]
    for o, t in zip(d31, fixed_last):
        o["time"] = t
    orders.sort(key=lambda o: (o["day"], o["time"]))
    for i, o in enumerate(orders):
        o["id"] = i + 1
    assert [o["time"] for o in orders[:5]] == fixed_first
    assert [o["time"] for o in orders[-3:]] == fixed_last

    # staff and payment
    first = [(3, "Card"), (1, "Card"), (4, "Card"), (1, "Cash"), (4, "Cash")]
    staff = Counter(STAFF_ORDERS)
    pay = Counter({"Card": CARD, "Cash": CASH})
    for s, p in first:
        staff[s] -= 1
        pay[p] -= 1
    sl = [s for s, n in staff.items() for _ in range(n)]
    pl = [p for p, n in pay.items() for _ in range(n)]
    rng.shuffle(sl)
    rng.shuffle(pl)
    for o, (s, p) in zip(orders, first + list(zip(sl, pl))):
        o["staff"], o["payment"] = s, p
    # cash on 1 March: served by exactly Sam, Priya, Mia and Ali
    day1 = [o for o in orders if o["day"] == 1]
    for o in day1[5:]:
        if o["payment"] == "Cash" and o["staff"] == 3:
            sw = next(x for x in day1[5:] if x["payment"] == "Card" and x["staff"] != 3)
            o["staff"], sw["staff"] = sw["staff"], o["staff"]
    for need in (2, 5):
        if not any(o["payment"] == "Cash" and o["staff"] == need for o in day1):
            cash = [o for o in day1[5:] if o["payment"] == "Cash"]
            target = next((o for o in cash if [x["staff"] for x in day1 if x["payment"] == "Cash"].count(o["staff"]) > 1), None)
            if target is None:  # make another cash order
                target = next(o for o in day1[5:] if o["payment"] == "Card")
                other = next(o for o in orders if o["day"] > 1 and o["payment"] == "Cash")
                target["payment"], other["payment"] = "Cash", "Card"
            sw = next(x for x in orders if x["day"] > 1 and x["staff"] == need)
            target["staff"], sw["staff"] = need, target["staff"]
    assert {o["staff"] for o in day1 if o["payment"] == "Cash"} == {1, 2, 4, 5}

    # loyalty customers
    counts = dict(CUST_ORDERS)
    others = [n for n in CUSTOMERS if n not in counts]
    left = LOYALTY - sum(counts.values())
    base = [rng.randint(9, 25) for _ in others]
    scale = left / sum(base)
    alloc = [max(6, round(b * scale)) for b in base]
    while sum(alloc) != left:
        i = rng.randrange(len(alloc))
        alloc[i] += 1 if sum(alloc) < left else (-1 if alloc[i] > 6 else 0)
    counts.update(zip(others, alloc))
    pool = [n for n, k in counts.items() for _ in range(k)]
    slots = rng.sample(orders[5:], LOYALTY)
    for o, n in zip(slots, pool):
        o["customer"] = CID[n]
    for o in orders:
        o.setdefault("customer", None)
    if not any(o["customer"] == CID["Aisha Tran"] and o["day"] <= 7 for o in orders):
        a = next(o for o in orders if o["customer"] == CID["Aisha Tran"])
        b = next(o for o in orders[5:] if o["day"] <= 7 and o["customer"] is None)
        a["customer"], b["customer"] = None, CID["Aisha Tran"]
    return orders


def build_lines(orders):
    # lines per item and their quantities
    ratio = {1: 1.28, 2: 1.26, 3: 1.25, 4: 1.2, 5: 1.15, 6: 1.12, 7: 1.2, 8: 1.12,
             9: 1.1, 10: 1.18, 11: 1.15, 12: 1.12, 13: 1.18, 14: 1.12}
    nlines = {i: max(1, round(MENU[i - 1][5] / r)) for i, r in ratio.items()}
    while sum(nlines.values()) != TOTAL_LINES:
        i = rng.choice(list(nlines))
        nlines[i] += 1 if sum(nlines.values()) < TOTAL_LINES else -1
        nlines[i] = min(nlines[i], MENU[i - 1][5])
    lines = []
    for i, n in nlines.items():
        q = [1] * n
        for _ in range(MENU[i - 1][5] - n):
            j = rng.randrange(n)
            while q[j] >= 4:
                j = rng.randrange(n)
            q[j] += 1
        lines += [[i, x] for x in q]
    # fixed: order 2 = hot chocolate + muffin, order 5 = two flat whites
    def take(item, qty):
        k = next(k for k, l in enumerate(lines) if l == [item, qty])
        return lines.pop(k)
    fixed = {2: [take(7, 1), take(13, 1)], 5: [take(1, 2)]}
    rng.shuffle(lines)
    # lines per order
    free = [o for o in orders if o["id"] not in fixed]
    per = {o["id"]: 1 for o in free}
    extra = len(lines) - len(free)
    while extra:
        o = rng.choice(free)
        if per[o["id"]] < 4:
            per[o["id"]] += 1
            extra -= 1
    out = {k: [l + [True] for l in v] for k, v in fixed.items()}
    it = iter(lines)
    for o in free:
        out[o["id"]] = [next(it) + [False] for _ in range(per[o["id"]])]
    # no item twice in one order
    flat = [(oid, l) for oid, ls in out.items() for l in ls if not l[2]]
    def dup(oid):
        items = [l[0] for l in out[oid]]
        return len(items) != len(set(items))
    for oid in list(out):
        while dup(oid):
            items = [l[0] for l in out[oid]]
            l = next(l for l in out[oid] if items.count(l[0]) > 1 and not l[2])
            oid2, l2 = rng.choice(flat)
            if l2[1] != l[1] or oid2 == oid or l[0] in [x[0] for x in out[oid2]] or l2[0] in items:
                continue
            l[0], l2[0] = l2[0], l[0]
    return out


def fit(orders, out):
    """Swap items between lines with the same quantity until the day and
    customer totals match the lessons. Item totals never change."""
    oday = {o["id"]: o["day"] for o in orders}
    ocust = {o["id"]: o["customer"] for o in orders}
    name = {CID[n]: n for n in CUSTOMERS}
    val = {oid: sum(PRICE[l[0]] * l[1] for l in ls) for oid, ls in out.items()}
    day = defaultdict(int)
    cust = defaultdict(int)
    for oid, v in val.items():
        day[oday[oid]] += v
        if ocust[oid]:
            cust[ocust[oid]] += v

    def dcost(d, v):
        if d in DAY_TAKINGS:
            return abs(v - DAY_TAKINGS[d]) * 3
        return max(0, DAY_MIN - v) + max(0, v - DAY_MAX)

    def ccost(c, v):
        n = name[c]
        if n in CUST_SPEND:
            return abs(v - CUST_SPEND[n]) * 3
        return max(0, v - CUST_MAX_OTHER)

    def total():
        return sum(dcost(d, day[d]) for d in range(1, 32)) + sum(ccost(c, v) for c, v in cust.items())

    bylen = defaultdict(list)
    for oid, ls in out.items():
        for l in ls:
            if not l[2]:
                bylen[l[1]].append((oid, l))
    cost = total()
    step = 0
    while cost > 0:
        step += 1
        q = rng.choice([1, 1, 1, 2])
        (oa, la), (ob, lb) = rng.sample(bylen[q], 2)
        if oa == ob or la[0] == lb[0]:
            continue
        if la[0] in [x[0] for x in out[ob]] or lb[0] in [x[0] for x in out[oa]]:
            continue
        delta = q * (PRICE[lb[0]] - PRICE[la[0]])  # oa gains delta, ob loses it
        da, db, ca, cb = oday[oa], oday[ob], ocust[oa], ocust[ob]
        changes = defaultdict(int)
        changes[("d", da)] += delta
        changes[("d", db)] -= delta
        if ca:
            changes[("c", ca)] += delta
        if cb:
            changes[("c", cb)] -= delta
        before = after = 0
        for (k, key), ch in changes.items():
            if ch == 0:
                continue
            if k == "d":
                before += dcost(key, day[key]); after += dcost(key, day[key] + ch)
            else:
                before += ccost(key, cust[key]); after += ccost(key, cust[key] + ch)
        temp = max(0.05, 2.0 * (1 - step / 3_000_000))
        if after < before or rng.random() < math.exp(-(after - before + 0.5) / temp):
            la[0], lb[0] = lb[0], la[0]
            for (k, key), ch in changes.items():
                (day if k == "d" else cust)[key] += ch
            cost += after - before
        if step > 5_000_000:
            raise SystemExit(f"could not fit, cost {cost}")
    return day, cust


def money(v):
    return f"{v // 10}.{v % 10}0"


def main(path):
    orders = build_orders()
    out = build_lines(orders)
    fit(orders, out)
    q = lambda s: "'" + s.replace("'", "''") + "'"
    w = []
    w.append("-- Corner Café: sales database for PostgreSQL Foundations (Avro Academy)")
    w.append("-- A made-up café, made-up people. March 2026.")
    w.append("-- Run it in psql with:  \\i cafe.sql")
    w.append("-- Running it again puts everything back to how it started.")
    w.append("")
    w.append("DROP TABLE IF EXISTS order_items, orders, customers, staff, menu_items, categories;")
    w.append("""
CREATE TABLE categories (
  id   integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  name text NOT NULL UNIQUE
);

CREATE TABLE menu_items (
  id          integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  name        text NOT NULL UNIQUE,
  category_id integer NOT NULL REFERENCES categories (id),
  price       numeric(5, 2) NOT NULL CHECK (price > 0),
  vegetarian  boolean NOT NULL DEFAULT false,
  available   boolean NOT NULL DEFAULT true
);

CREATE TABLE staff (
  id          integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  first_name  text NOT NULL,
  last_name   text NOT NULL,
  role        text NOT NULL,
  hourly_rate numeric(5, 2) NOT NULL CHECK (hourly_rate > 0),
  started_on  date NOT NULL
);

CREATE TABLE customers (
  id        integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  name      text NOT NULL,
  email     text UNIQUE,
  phone     text,
  joined_on date NOT NULL DEFAULT current_date
);

CREATE TABLE orders (
  id          integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  ordered_at  timestamp NOT NULL,
  staff_id    integer NOT NULL REFERENCES staff (id),
  customer_id integer REFERENCES customers (id),
  payment     text NOT NULL CHECK (payment IN ('Card', 'Cash'))
);

CREATE TABLE order_items (
  order_id     integer NOT NULL REFERENCES orders (id) ON DELETE CASCADE,
  menu_item_id integer NOT NULL REFERENCES menu_items (id),
  quantity     integer NOT NULL CHECK (quantity > 0),
  unit_price   numeric(5, 2) NOT NULL CHECK (unit_price >= 0),
  PRIMARY KEY (order_id, menu_item_id)
);
""")
    w.append("INSERT INTO categories (name) VALUES\n" + ",\n".join(f"  ({q(c)})" for c in CATEGORIES) + ";\n")
    w.append("INSERT INTO menu_items (name, category_id, price, vegetarian, available) VALUES\n" + ",\n".join(
        f"  ({q(m[0])}, {m[1]}, {m[2]}, {str(m[3]).lower()}, {str(m[4]).lower()})" for m in MENU) + ";\n")
    w.append("INSERT INTO staff (first_name, last_name, role, hourly_rate, started_on) VALUES\n" + ",\n".join(
        f"  ({q(s[0])}, {q(s[1])}, {q(s[2])}, {s[3]}, '{s[4]}')" for s in STAFF) + ";\n")
    crow = []
    r2 = random.Random(7)
    for i, n in enumerate(CUSTOMERS):
        email = "NULL" if n in NO_EMAIL else q(n.lower().replace(" ", ".") + "@example.com")
        phone = q(f"04{r2.randint(10, 99)} 555 {i + 1:03d}")
        if n in JOINED:
            joined = JOINED[n]
        else:
            joined = f"20{r2.choice([24, 25, 25, 25])}-{r2.randint(1, 12):02d}-{r2.randint(1, 28):02d}"
        crow.append(f"  ({q(n)}, {email}, {phone}, '{joined}')")
    w.append("INSERT INTO customers (name, email, phone, joined_on) VALUES\n" + ",\n".join(crow) + ";\n")
    w.append("INSERT INTO orders (ordered_at, staff_id, customer_id, payment) VALUES\n" + ",\n".join(
        f"  ('2026-03-{o['day']:02d} {o['time']}', {o['staff']}, {o['customer'] or 'NULL'}, '{o['payment']}')"
        for o in orders) + ";\n")
    rows = []
    for oid in sorted(out):
        for item, qty, _ in sorted(out[oid]):
            rows.append(f"  ({oid}, {item}, {qty}, {MENU[item - 1][2]})")
    w.append("INSERT INTO order_items (order_id, menu_item_id, quantity, unit_price) VALUES\n" + ",\n".join(rows) + ";\n")
    w.append("ANALYZE;\n")
    with open(path, "w") as f:
        f.write("\n".join(w))


if __name__ == "__main__":
    main(sys.argv[1])
