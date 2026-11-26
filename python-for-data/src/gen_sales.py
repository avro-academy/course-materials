"""Generates the Corner Café 2025 sales data so every output shown in the Python for Data lessons is reproduced exactly.
Writes ../build/starter/data/{cafe_sales_2025.csv, products.csv}. Deterministic (seeded)."""
import csv, datetime as dt, math, os, random
from collections import Counter, defaultdict
random.seed(2025)
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'build', 'starter', 'data')
os.makedirs(OUT, exist_ok=True)
# item: (category, price in dimes, cost, total qty, clean lines)
ITEMS = {
 'Flat white': ('Coffee', 48, 1.10, 1495, 1045), 'Latte': ('Coffee', 48, 1.15, 1145, 800),
 'Cappuccino': ('Coffee', 48, 1.10, 822, 575), 'Long black': ('Coffee', 42, 0.80, 544, 380),
 'Chai latte': ('Tea', 52, 0.90, 478, 330), 'English breakfast tea': ('Tea', 40, 0.40, 314, 220),
 'Hot chocolate': ('Drinks', 50, 1.00, 520, 367), 'Mixed berry smoothie': ('Drinks', 75, 1.80, 210, 148),
 'Orange juice': ('Drinks', 55, 1.90, 403, 285), 'Banana bread': ('Food', 55, 1.40, 650, 472),
 'Ham and cheese toastie': ('Food', 95, 3.20, 567, 354), 'Veggie wrap': ('Food', 110, 3.90, 388, 270),
 'Lemon slice': ('Food', 45, 1.10, 411, 306), 'Raspberry muffin': ('Food', 50, 1.30, 297, 207)}
assert sum(v[4] for v in ITEMS.values()) == 5759
CATS = ['Coffee', 'Drinks', 'Food', 'Tea']
# ---- quantities: global multiset for clean lines
QCOUNT = {1: 3967, 2: 1310, 3: 305, 4: 150, 5: 20, 6: 7}
chunks = [k - 1 for k, c in QCOUNT.items() for _ in range(c) if k > 1]
chunks.sort(reverse=True)
need = {i: v[3] - v[4] for i, v in ITEMS.items()}
assert sum(need.values()) == sum(chunks)
alloc = defaultdict(list)
for i, ch, n in [('English breakfast tea', 3, 8), ('Chai latte', 2, 10)]:  # tea needs some 4 x EBT and 3 x chai lines (156 vs 160)
    for _ in range(n): chunks.remove(ch); alloc[i].append(ch); need[i] -= ch
for ch in chunks:  # give each chunk to the item with most remaining need that can take it
    cands = [i for i in ITEMS if need[i] >= ch and len(alloc[i]) < ITEMS[i][4]]
    i = max(cands, key=lambda i: need[i] + random.random())
    alloc[i].append(ch); need[i] -= ch
assert all(v == 0 for v in need.values()), need
lines = []  # each: dict
for i, (cat, p, cost, q, n) in ITEMS.items():
    qs = [c + 1 for c in alloc[i]] + [1] * (n - len(alloc[i]))
    for x in qs: lines.append({'item': i, 'category': cat, 'price': p, 'qty': x, 'rev': p * x})
random.shuffle(lines)
assert Counter(l['qty'] for l in lines) == Counter(QCOUNT)
# ---- targets (dimes)
D = lambda x: round(x * 10)
MONTH = [D(x) for x in [3355.9, 3292.5, 3812.2, 3463.4, 3963.2, 4296.0, 4567.5, 4539.7, 3450.1, 3563.5, 4128.6, 3166.9]]
WDAY = [D(x) for x in [5446.7, 5455.7, 5784.6, 5386.9, 5902.9, 8776.6, 8846.1]]
QCAT = {('Coffee', 0): 4518.6, ('Coffee', 1): 4947.0, ('Coffee', 2): 4849.8, ('Coffee', 3): 4587.0,
        ('Drinks', 0): 1371.5, ('Drinks', 1): 1538.0, ('Drinks', 2): 1956.0, ('Drinks', 3): 1526.0,
        ('Food', 0): 3618.5, ('Food', 1): 4242.0, ('Food', 2): 4779.5, ('Food', 3): 3924.0,
        ('Tea', 0): 952.0, ('Tea', 1): 995.6, ('Tea', 2): 972.0, ('Tea', 3): 822.0}
QCAT = {k: D(v) for k, v in QCAT.items()}
for c in CATS:
    assert sum(QCAT[(c, q)] for q in range(4)) == sum(l['rev'] for l in lines if l['category'] == c), c
# ---- 1 January: 14 fixed lines (first five shown in the lesson), total $113.80
days = [dt.date(2025, 1, 1) + dt.timedelta(d) for d in range(365)]
def take(item, qty):
    for k, l in enumerate(lines):
        if l['item'] == item and l['qty'] == qty and 'date' not in l: return l
    raise SystemExit(f'no {item} x{qty}')
first5 = [take(*x) for x in [('Chai latte', 1), ('English breakfast tea', 2), ('Hot chocolate', 2), ('Orange juice', 1), ('Lemon slice', 1)]]
for l in first5: l['date'] = days[0]
rest9 = [('Flat white', 2), ('Latte', 1), ('Cappuccino', 1), ('Ham and cheese toastie', 1), ('Veggie wrap', 1), ('Banana bread', 2), ('Lemon slice', 1), ('Chai latte', 2), ('Mixed berry smoothie', 2)]
jan1 = first5 + [take(*x) for x in rest9]
for l in jan1: l['date'] = days[0]; l['fixed'] = True
assert sum(l['rev'] for l in jan1) == 1138, sum(l['rev'] for l in jan1)
# ---- month x category targets (dimes): rows hit the monthly totals, quarters hit the pivot table
MOD = {'Coffee': 6, 'Tea': 4, 'Drinks': 5, 'Food': 5}
M = {}
for q in range(4):
    months = [3 * q + 1, 3 * q + 2, 3 * q + 3]
    qtot = sum(MONTH[m - 1] for m in months)
    for m in months[:2]:
        share = MONTH[m - 1] / qtot
        for c in ['Coffee', 'Tea', 'Drinks']:
            M[(m, c)] = round(QCAT[(c, q)] * share / MOD[c]) * MOD[c]
        while (MONTH[m - 1] - M[(m, 'Coffee')] - M[(m, 'Tea')] - M[(m, 'Drinks')]) % 5: M[(m, 'Coffee')] += 6
        M[(m, 'Food')] = MONTH[m - 1] - M[(m, 'Coffee')] - M[(m, 'Tea')] - M[(m, 'Drinks')]
    for c in CATS:
        M[(months[2], c)] = QCAT[(c, q)] - M[(months[0], c)] - M[(months[1], c)]
for m in range(1, 13): assert sum(M[(m, c)] for c in CATS) == MONTH[m - 1]
# ---- phase A: give each line a month so every month x category cell is exact (1 Jan lines are fixed in January)
for c in ['Tea', 'Drinks', 'Coffee', 'Food']:
    ls = [l for l in lines if l['category'] == c]
    tot = {m: 0 for m in range(1, 13)}
    for l in ls:
        if l.get('fixed'): l['month'] = 1; tot[1] += l['rev']
    free = [l for l in ls if not l.get('fixed')]
    random.shuffle(free)
    for l in free:  # greedy: month furthest below target
        m = max(tot, key=lambda m: (M[(m, c)] - tot[m]) / max(M[(m, c)], 1))
        l['month'] = m; tot[m] += l['rev']
    cst = lambda: sum(abs(tot[m] - M[(m, c)]) for m in tot)
    c0 = cst(); it = 0
    while c0:
        it += 1
        x, y = random.sample(free, 2)
        if random.random() < 0.3:  # move one line to another month
            mx, mt = x['month'], random.randint(1, 12)
            if mx == mt: continue
            before = abs(tot[mx] - M[(mx, c)]) + abs(tot[mt] - M[(mt, c)])
            after = abs(tot[mx] - x['rev'] - M[(mx, c)]) + abs(tot[mt] + x['rev'] - M[(mt, c)])
            if after <= before or random.random() < 0.002:
                tot[mx] -= x['rev']; tot[mt] += x['rev']; x['month'] = mt; c0 += after - before
            continue
        if x['month'] == y['month'] or x['rev'] == y['rev']: continue
        mx, my = x['month'], y['month']
        before = abs(tot[mx] - M[(mx, c)]) + abs(tot[my] - M[(my, c)])
        d = y['rev'] - x['rev']
        after = abs(tot[mx] + d - M[(mx, c)]) + abs(tot[my] - d - M[(my, c)])
        if after <= before or random.random() < 0.001:
            tot[mx] += d; tot[my] -= d; x['month'], y['month'] = my, mx; c0 += after - before
        if it > 300_000: break
    tabu = []
    for rnd in range(5000):  # endgame: exhaustive over (month, revenue) signatures, with a short tabu list
        if c0 == 0: break
        sig = {}
        for l in free: sig.setdefault((l['month'], l['rev']), []).append(l)
        keys = list(sig); opts = []
        r = {m: tot[m] - M[(m, c)] for m in tot}
        for (ma, ra) in keys:
            for mt in range(1, 13):  # single move
                if mt != ma:
                    dl = abs(r[ma] - ra) + abs(r[mt] + ra) - abs(r[ma]) - abs(r[mt])
                    opts.append((dl, ('mv', (ma, ra), mt)))
            for (mb, rb) in keys:
                if mb > ma and ra != rb:
                    d = rb - ra
                    dl = abs(r[ma] + d) + abs(r[mb] - d) - abs(r[ma]) - abs(r[mb])
                    opts.append((dl, ('sw', (ma, ra), (mb, rb))))
        opts = [o for o in opts if o[1] not in tabu]
        opts.sort(key=lambda o: (o[0], random.random()))
        dl, mv = opts[0]
        tabu = (tabu + [mv])[-30:]
        if mv[0] == 'mv':
            x = sig[mv[1]][0]; tot[x['month']] -= x['rev']; tot[mv[2]] += x['rev']; x['month'] = mv[2]
        else:
            x = sig[mv[1]][0]; y = sig[mv[2]][0]; d = y['rev'] - x['rev']
            tot[x['month']] += d; tot[y['month']] -= d; x['month'], y['month'] = y['month'], x['month']
        c0 = cst()
    if c0 and c == 'Tea':  # keep what tea reached; move the difference into coffee (+1.5r) and food (-2.5r) in the same month
        for m in tot:
            r = tot[m] - M[(m, c)]
            M[(m, 'Tea')] += r; M[(m, 'Coffee')] += 3 * r // 2; M[(m, 'Food')] -= 5 * r // 2
        for m in range(1, 13): assert sum(M[(m, k)] for k in CATS) == MONTH[m - 1]
        for k in CATS:
            for q in range(4): assert sum(M[(m, k)] for m in (3*q+1, 3*q+2, 3*q+3)) == QCAT[(k, q)], (k, q)
        c0 = 0
    if c0: print({m: (tot[m], M[(m, c)]) for m in tot}); raise SystemExit(f'phase A {c} stuck at {c0}')
    print('phase A', c, 'solved after', it)
# ---- lines per day within each month: busier on weekends (in proportion to the weekday totals)
wdays = Counter(d.weekday() for d in days)
for m in range(1, 13):
    md = [d for d in days if d.month == m and d != days[0]]
    ls = [l for l in lines if l['month'] == m and not l.get('fixed')]
    w = [WDAY[d.weekday()] / wdays[d.weekday()] for d in md]
    raw = [x / sum(w) * len(ls) for x in w]
    cnt = [int(x) for x in raw]
    for k in sorted(range(len(md)), key=lambda k: raw[k] - cnt[k], reverse=True)[:len(ls) - sum(cnt)]: cnt[k] += 1
    random.shuffle(ls); k = 0
    for d, n in zip(md, cnt):
        for _ in range(n): ls[k]['date'] = d; k += 1
# ---- phase B: swap dates inside a month (keeps every month and quarter total) until the weekday totals are exact
ws = [0] * 7
for l in lines: ws[l['date'].weekday()] += l['rev']
bymonth = defaultdict(list)
for l in lines:
    if not l.get('fixed'): bymonth[l['month']].append(l)
c0 = sum(abs(a - b) for a, b in zip(ws, WDAY)); it = 0
while c0:
    it += 1
    ls = bymonth[random.randint(1, 12)]
    x, y = random.sample(ls, 2)
    wx, wy = x['date'].weekday(), y['date'].weekday()
    if wx == wy or x['rev'] == y['rev']: continue
    d = y['rev'] - x['rev']
    before = abs(ws[wx] - WDAY[wx]) + abs(ws[wy] - WDAY[wy])
    after = abs(ws[wx] + d - WDAY[wx]) + abs(ws[wy] - d - WDAY[wy])
    if after <= before:
        ws[wx] += d; ws[wy] -= d; x['date'], y['date'] = y['date'], x['date']; c0 += after - before
    if it > 3_000_000: raise SystemExit(f'phase B stuck at {c0}')
print('phase B solved after', it)
# ---- staff: exact lines, then exact revenue by swapping labels
STAFF = {'Ali': (1174, D(9195.5)), 'Jordan': (1157, D(9033.2)), 'Mel': (1185, D(9451.1)), 'Priya': (1124, D(8848.5)), 'Sam': (1119, D(9071.2))}
labels = [s for s, (n, _) in STAFF.items() for _ in range(n)]; random.shuffle(labels)
for l, s in zip(lines, labels): l['staff'] = s
sr = defaultdict(int)
for l in lines: sr[l['staff']] += l['rev']
sc = lambda: sum(abs(sr[s] - STAFF[s][1]) for s in STAFF)
c0 = sc(); it = 0
while c0 > 0:
    it += 1; a, b = random.sample(lines, 2)
    if a['staff'] == b['staff'] or a['rev'] == b['rev']: continue
    sr[a['staff']] += b['rev'] - a['rev']; sr[b['staff']] += a['rev'] - b['rev']; a['staff'], b['staff'] = b['staff'], a['staff']
    c1 = sc()
    if c1 <= c0: c0 = c1
    else:
        sr[a['staff']] += b['rev'] - a['rev']; sr[b['staff']] += a['rev'] - b['rev']; a['staff'], b['staff'] = b['staff'], a['staff']
print('staff solved after', it)
# ---- payments: exact per category (clean): Card / Cash / Unknown
PAY = {'Coffee': (2408, 366, 26), 'Drinks': (686, 106, 8), 'Food': (1368, 225, 16), 'Tea': (461, 82, 7)}
for c, (card, cash, unk) in PAY.items():
    ls = [l for l in lines if l['category'] == c]; assert len(ls) == card + cash + unk, c
    p = ['Card'] * card + ['Cash'] * cash + [None] * unk; random.shuffle(p)
    for l, x in zip(ls, p): l['pay'] = x
# Sam's clean cash lines must be 154 - dirty Sam cash (set below to 3) = 151: swap payments within a category between Sam and others
def samcash(): return sum(1 for l in lines if l['staff'] == 'Sam' and l['pay'] == 'Cash')
while samcash() != 151:
    up = samcash() < 151
    a = random.choice([l for l in lines if l['staff'] == 'Sam' and (l['pay'] != 'Cash') == up])
    b = random.choice([l for l in lines if l['staff'] != 'Sam' and l['category'] == a['category'] and (l['pay'] == 'Cash') == up])
    a['pay'], b['pay'] = b['pay'], a['pay']
for l in jan1:  # the five rows shown are all paid by card; keep 1 Jan simple
    if l['pay'] != 'Card':
        b = next(x for x in lines if x['category'] == l['category'] and x['pay'] == 'Card' and x['staff'] == l['staff'] and not x.get('fixed'))
        l['pay'], b['pay'] = b['pay'], l['pay']
# ---- times: hour weights per day, minutes random; busiest hour 8
HW = {7: 8, 8: 17, 9: 15, 10: 11, 11: 8, 12: 13, 13: 10, 14: 6, 15: 4}
for l in lines:
    h = random.choices(list(HW), weights=list(HW.values()))[0]
    l['time'] = f'{h:02d}:{random.randint(0, 59):02d}'
for k, l in enumerate(first5): l['time'] = f'07:{5 + 4 * k:02d}'
for l in jan1[5:]:
    if l['time'] < '07:30': l['time'] = '07:4' + l['time'][-1]
import pickle
pickle.dump((lines, jan1, first5), open('/tmp/claude-0/-home-user/24ebfbb1-feb6-557b-9f42-e1b816719782/scratchpad/clean_lines.pkl', 'wb'))
print('clean lines ready', len(lines))
# =====================================================================================
# Part 2: the raw till export with its problems
# =====================================================================================
PRICE = {i: v[1] / 10 for i, v in ITEMS.items()}
def money(p): return f'${p:.2f}'
for l in lines:
    l['istr'] = l['item']; l['pstr'] = money(PRICE[l['item']]); l['paystr'] = l['pay']
early = [l for l in lines if l['date'] < dt.date(2025, 6, 1)]
X = len(early)
n_nan_early = 2354 - X - 9
print('clean lines Jan-May', X, '-> NaN rows before June:', n_nan_early)
assert 0 <= n_nan_early <= 87
# 18 duplicates: 9 x qty 4 and 9 x qty 3, nine before June
def pick_dups(pool, n, qty, items):
    out = []
    for it_ in items:
        cand = [l for l in pool if l['qty'] == qty and l['item'] == it_ and not l.get('fixed') and l not in out]
        cand = cand or [l for l in pool if l['qty'] == qty and not l.get('fixed') and l not in out]
        out.append(random.choice(cand))
    return out
late = [l for l in lines if l['date'] >= dt.date(2025, 6, 1)]
dups = (pick_dups(early, 5, 4, ['Latte', 'Flat white', 'Ham and cheese toastie', 'Banana bread', 'Latte'])
        + pick_dups(early, 4, 3, ['Cappuccino', 'Hot chocolate', 'Latte', 'Veggie wrap'])
        + pick_dups(late, 4, 4, ['Latte', 'Flat white', 'Orange juice', 'Chai latte'])
        + pick_dups(late, 5, 3, ['Latte', 'Banana bread', 'Lemon slice', 'Flat white', 'Long black']))
assert len(set(map(id, dups))) == 18
# 87 rows with a blank quantity (new orders) + 1 typo row
def nan_row(item, date):
    return {'item': item, 'category': ITEMS[item][0], 'price': ITEMS[item][1], 'qty': None, 'rev': 0, 'date': date,
            'staff': random.choice(list(STAFF)), 'time': f"{random.choices(list(HW), weights=list(HW.values()))[0]:02d}:{random.randint(0, 59):02d}",
            'istr': item, 'pstr': money(PRICE[item]), 'nan': True}
dup_latte = sum(1 for l in dups if l['item'] == 'Latte'); dup_chai = sum(1 for l in dups if l['item'] == 'Chai latte')
dup_ct = sum(1 for l in dups if ITEMS[l['item']][0] in ('Coffee', 'Tea'))
nan_items = (['Latte'] * (35 - dup_latte) + ['Chai latte'] * (9 - dup_chai))
ct_left = 66 - 1 - dup_ct - len(nan_items)  # other coffee/tea NaN rows (the typo is a Cappuccino)
nan_items += random.choices(['Flat white', 'Cappuccino', 'Long black', 'English breakfast tea'], k=ct_left)
nan_items += random.choices(['Hot chocolate', 'Orange juice', 'Mixed berry smoothie', 'Banana bread', 'Ham and cheese toastie', 'Veggie wrap', 'Lemon slice', 'Raspberry muffin'], k=87 - len(nan_items))
random.shuffle(nan_items)
early_days = [d for d in days if dt.date(2025, 1, 2) <= d < dt.date(2025, 6, 1)]
late_days = [d for d in days if d > dt.date(2025, 6, 1)]
nans = [nan_row(it_, random.choice(early_days if k < n_nan_early else late_days)) for k, it_ in enumerate(nan_items)]
typo = {'item': 'Cappuccino', 'category': 'Coffee', 'price': 48, 'qty': 120, 'rev': 0, 'date': dt.date(2025, 6, 1), 'staff': 'Mel',
        'time': '07:02', 'istr': 'Cappuccino', 'pstr': '$4.80', 'paystr': 'Card', 'typo': True}
# tune the average raw unit price to $5.50 (to 2 places) by swapping NaN-row foods/drinks
def avg_price():
    ps = [PRICE[l['item']] for l in lines] + [PRICE[l['item']] for l in dups] + [PRICE[l['item']] for l in nans] + [4.8]
    return sum(ps) / len(ps)
swappable = [n for n in nans if ITEMS[n['item']][0] in ('Drinks', 'Food')]
while not 5.4955 <= avg_price() <= 5.5045:
    n = random.choice(swappable)
    n['item'] = random.choice(['Lemon slice', 'Raspberry muffin', 'Hot chocolate']) if avg_price() > 5.5 else random.choice(['Ham and cheese toastie', 'Veggie wrap', 'Mixed berry smoothie'])
    n['category'] = ITEMS[n['item']][0]; n['istr'] = n['item']; n['pstr'] = money(PRICE[n['item']])
print('average raw unit price', round(avg_price(), 4))
# payments of the dirty rows: dups copy their originals; NaN rows get the rest so dirt = 88 card, 17 cash, 1 blank
dpay = Counter(l['pay'] for l in dups); dpay['Card'] += 1  # typo row is Card
need_card, need_cash, need_none = 88 - dpay['Card'], 17 - dpay['Cash'], 1 - dpay[None]
assert min(need_card, need_cash, need_none) >= 0, dpay
pp = ['Card'] * need_card + ['Cash'] * need_cash + [None] * need_none; random.shuffle(pp)
for n, p in zip(nans, pp): n['pay'] = n['paystr'] = p
# Sam's dirty cash rows must be 3 (clean has 151)
def dirty_samcash(): return sum(1 for l in dups + nans if l['staff'] == 'Sam' and l['pay'] == 'Cash')
while dirty_samcash() != 3:
    cash_nans = [n for n in nans if n['pay'] == 'Cash']
    n = random.choice(cash_nans)
    n['staff'] = 'Sam' if dirty_samcash() < 3 else random.choice(['Ali', 'Jordan', 'Mel', 'Priya'])
# ---- assemble rows, sorted by date and time; duplicates follow their originals
rows = lines + nans + [typo]
for r in rows: r.setdefault('paystr', r.get('pay'))
rows.sort(key=lambda r: (r['date'], r['time'], 0 if r in first5 else 1, first5.index(r) if r in first5 else 0))
# the typo row is the first line on 1 June; the five lesson rows open 1 January
june = [r for r in rows if r['date'] == dt.date(2025, 6, 1)]
for r in june:
    if r is not typo and r['time'] <= '07:02': r['time'] = '07:1' + r['time'][-1]
rows.sort(key=lambda r: (r['date'], r['time'], first5.index(r) if r in first5 else 9))
assert rows[:5] == first5, [r['item'] for r in rows[:5]]
# ---- text problems: item spellings, payment capitals, prices without $ (dups copy their original afterwards)
dupids = {id(d) for d in dups}
cands = [r for r in rows if not r.get('fixed') and r is not typo and id(r) not in dupids]
def mark(item, field, value, n):
    pool = [r for r in cands if r['item'] == item and r[field] == (item if field == 'istr' else r[field]) and not r.get('_v')]
    for r in random.sample(pool, n): r[field] = value; r['_v'] = True
mark('Chai latte', 'istr', ' chai latte', 20 - sum(1 for d in dups if False))
mark('Chai latte', 'istr', 'Chai Latte', 20)
a_ = next(r for r in rows if r['istr'] in (' chai latte', 'Chai Latte'))
if a_['istr'] == 'Chai Latte':  # value_counts keeps ties in order of first appearance: ' chai latte' must come first
    b_ = next(r for r in rows if r['istr'] == ' chai latte'); a_['istr'], b_['istr'] = b_['istr'], a_['istr']
mark('Banana bread', 'istr', 'Banana Bread', 24)
mark('Flat white', 'istr', 'Flat White', 31)
mark('Flat white', 'istr', 'flat white', 17)
mark('Flat white', 'istr', 'Flat white ', 9)
mark('Veggie wrap', 'istr', 'Veggie Wrap', 14)
cardrows = [r for r in rows if r['paystr'] == 'Card' and r is not typo and r not in first5 and id(r) not in dupids]
for r in random.sample(cardrows, 173 + 62)[:173]: r['paystr'] = 'card'
for r in [r for r in cardrows if r['paystr'] == 'Card']: pass
rest = [r for r in cardrows if r['paystr'] == 'Card']
for r in random.sample(rest, 62): r['paystr'] = 'CARD'
for r in random.sample([r for r in rows if r not in first5 and r is not typo], 190): r['pstr'] = str(PRICE[r['item']])
first5[3]['pstr'] = '5.5'  # Orange juice on row 3 has no $ sign
# ---- write the raw CSV, with duplicates placed right after their originals
out = []
oid = 10000
dupset = {id(d) for d in dups}
for r in rows:
    oid += 1
    rec = [oid, r['date'].strftime('%d/%m/%Y'), r['time'], r['istr'], r['category'], '' if r['qty'] is None else r['qty'], r['pstr'], r['paystr'] or '', r['staff']]
    out.append(rec)
    if id(r) in dupset: out.append(list(rec))
with open(os.path.join(OUT, 'cafe_sales_2025.csv'), 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['order_id', 'date', 'time', 'item', 'category', 'quantity', 'unit_price', 'payment', 'staff']); w.writerows(out)
with open(os.path.join(OUT, 'products.csv'), 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['item', 'cost_price'])
    for it_ in ['Flat white', 'Latte', 'Cappuccino', 'Long black', 'Chai latte', 'English breakfast tea', 'Hot chocolate', 'Mixed berry smoothie',
                'Orange juice', 'Banana bread', 'Ham and cheese toastie', 'Veggie wrap', 'Lemon slice', 'Raspberry muffin']:
        w.writerow([it_, f'{ITEMS[it_][2]:.2f}'])
print('wrote', len(out), 'rows')
