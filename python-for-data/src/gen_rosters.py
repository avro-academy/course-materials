"""Generates data/rosters/roster_week_01..04.csv to match the roster report in Module 6."""
import csv, os, random
random.seed(7)
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'build', 'starter', 'data', 'rosters')
os.makedirs(OUT, exist_ok=True)
WD = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
# shift lengths per person: weekday, Saturday, Sunday (4 weeks)
PLAN = {
 'Priya': ([5.0, 7.5, 5.0, 5.0, 4.5, 5.0, 5.0, 5.0, 5.0, 5.0, 5.5, 5.0, 5.0, 5.0], [5.0], [7.0, 7.0, 7.5]),
 'Mel': ([5.0, 5.0, 5.0, 5.5, 5.0, 5.5, 5.0, 5.5, 5.0, 5.0], [5.0, 5.0, 5.0], [6.0, 6.5, 6.5]),
 'Sam': ([6.0, 6.0, 6.0, 6.5, 6.0, 6.0, 6.0], [6.0, 6.0], [4.5, 4.5, 4.5]),
 'Ali': ([5.5, 5.5, 6.0, 5.5, 6.0, 5.5], [4.5, 4.5, 5.0], [3.5, 4.0]),
 'Jordan': ([4.5, 4.5, 5.0], [4.5, 4.5, 5.0], [7.5]),
}
TARGET = {'Priya': (72.5, 5, 21.5), 'Mel': (51.5, 15, 19), 'Sam': (42.5, 12, 13.5), 'Ali': (34, 14, 7.5), 'Jordan': (14, 14, 7.5)}
for p, (w, sa, su) in PLAN.items():
    assert (sum(w), sum(sa), sum(su)) == TARGET[p], (p, sum(w), sum(sa), sum(su))
assert sum(len(v[0]) for v in PLAN.values()) == 40 and sum(len(v[1]) for v in PLAN.values()) == 12 and sum(len(v[2]) for v in PLAN.values()) == 12

def schedule():
    # slots: (week, day) -> list of (person, hours)
    slots = {(w, d): [] for w in range(4) for d in WD + ['Saturday', 'Sunday']}
    cap = {d: 2 for d in WD}; cap.update(Saturday=3, Sunday=3)
    # fixed start of week 1: Priya Mon 5.0, Sam Mon 6.0, Priya Tue 7.5
    pool = {p: [list(v[0]), list(v[1]), list(v[2])] for p, v in PLAN.items()}
    for p, d, h in [('Priya', 'Monday', 5.0), ('Sam', 'Monday', 6.0), ('Priya', 'Tuesday', 7.5)]:
        slots[(0, d)].append((p, h)); pool[p][0].remove(h)
    for kind, days in ((1, ['Saturday']), (2, ['Sunday']), (0, WD)):
        items = [(p, h) for p in pool for h in pool[p][kind]]
        random.shuffle(items)
        items.sort(key=lambda x: -sum(1 for q, _ in items if q == x[0]))  # busiest people first
        for p, h in items:
            opts = [(w, d) for w in range(4) for d in days if len(slots[(w, d)]) < cap[d] and p not in [q for q, _ in slots[(w, d)]]]
            if not opts: return None
            slots[random.choice(opts)].append((p, h))
    return slots

for _ in range(10000):
    s = schedule()
    if s: break
STARTS = {2: ['07:00', '10:30'], 3: ['07:00', '08:00', '11:00']}
def fmt(t): return f'{int(t):02d}:{int(round((t % 1) * 60)):02d}'
for w in range(4):
    rows = []
    for d in WD + ['Saturday', 'Sunday']:
        sh = s[(w, d)]
        if w == 0 and d == 'Monday': sh.sort(key=lambda x: x[0] != 'Priya')
        for k, (p, h) in enumerate(sh):
            if w == 0 and d == 'Monday': st = 7.0
            elif w == 0 and d == 'Tuesday' and p == 'Priya': st = 8.0
            else: st = [7.0, 9.0, 10.5][k] if len(sh) == 3 else [7.0, 16.0 - h][k]
            st = min(st, 16.5 - h)
            rows.append([p, d, fmt(st), fmt(st + h), f'{h:.1f}'])
    if w == 0:  # the lesson shows Priya Monday, Sam Monday, Priya Tuesday as the first three rows
        rows.sort(key=lambda r: (WD + ['Saturday', 'Sunday']).index(r[1]))
    with open(os.path.join(OUT, f'roster_week_{w + 1:02d}.csv'), 'w', newline='') as f:
        csv.writer(f).writerows([['name', 'day', 'start', 'finish', 'hours']] + rows)
print('rosters written')
