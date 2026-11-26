"""Generate the Bayside Paws insights data (72 posts, Jul–Sep 2026) so that
every figure quoted in the Social Media Marketing lessons comes out exactly.

Run: python gen_posts.py <out.csv>     (prints the lesson tables to compare)
"""
import csv
import math
import random
import sys
from datetime import date, timedelta

R = random.Random(7)
PILLARS = ["Grooming tips", "Happy dogs", "Behind the scenes", "Offers & news"]
FORMATS = ["Reel", "Carousel", "Photo", "Story"]
# posts per pillar x format (rows match the lesson's pillar counts, columns its format counts)
MATRIX = {
    "Grooming tips": [6, 11, 4, 2],
    "Happy dogs": [9, 3, 10, 4],
    "Behind the scenes": [3, 0, 4, 5],
    "Offers & news": [1, 2, 4, 4],
}
# lesson targets
T_P_REACH = {"Grooming tips": 1094, "Happy dogs": 891, "Behind the scenes": 914, "Offers & news": 1003}
T_P_ER = {"Grooming tips": 7.5, "Happy dogs": 7.8, "Behind the scenes": 6.5, "Offers & news": 2.8}
T_P_SAVES = {"Grooming tips": 26.7, "Happy dogs": 4.8, "Behind the scenes": 3.0, "Offers & news": 2.1}
T_P_CLICKS = {"Grooming tips": 10.1, "Happy dogs": 10.0, "Behind the scenes": 5.2, "Offers & news": 26.5}
T_P_BOOK = {"Grooming tips": 1, "Happy dogs": 4, "Behind the scenes": 1, "Offers & news": 8}
T_F_REACH = {"Reel": 1760, "Carousel": 936, "Photo": 693, "Story": 444}
T_F_ER = {"Reel": 6.6, "Carousel": 9.4, "Photo": 7.0, "Story": 3.6}
T_MONTH_BOOK = {7: 2, 8: 4, 9: 8}
T_SEP_CLICKS = 365

IDEAS = {
    ("Grooming tips", "Carousel"): ["How often should you groom your dog?", "Brushing curly coats at home: 5 steps", "Is your dog's coat matted? How to tell",
                                     "Your puppy's first groom: what to expect", "Bath time at home: what to use", "5 signs your dog needs a groom",
                                     "Winter coat care for curly breeds", "Checking ears after a swim", "How to choose the right brush",
                                     "Nails too long? The tap test", "Shedding season survival guide"],
    ("Grooming tips", "Reel"): ["How to check if your dog's nails are too long", "Brushing a cavoodle in 30 seconds", "Line brushing, the groomer's way",
                                 "Drying your dog without the drama", "Detangling spray: does it work?", "Paw balm in 15 seconds"],
    ("Grooming tips", "Photo"): ["The 4 brushes we use most", "Why we never shave double coats", "Tear stains: what helps", "Our favourite soap-free shampoo"],
    ("Grooming tips", "Story"): ["Poll: how often do you brush?", "Quick tip: wipe paws after the beach"],
    ("Happy dogs", "Reel"): ["Archie the spoodle: before and after", "Luna's first bath, slowed down", "Teddy-bear trim time-lapse", "Max the senior lab's spa day",
                              "Bella's summer clip reveal", "Three fluffy friends, one Saturday", "Puppy Coco meets the dryer", "Rocky's shaggy-to-sharp glow-up",
                              "Zero to fluffy in 20 seconds"],
    ("Happy dogs", "Carousel"): ["This week's happy customers", "Before and afters: July favourites", "Regulars of the month"],
    ("Happy dogs", "Photo"): ["Meet Biscuit after his teddy-bear trim", "Daisy's 10th birthday groom", "Ollie the groodle, fresh and fluffy", "Pepper's first groom",
                               "Milo the shih tzu's summer clip", "Rosie the cocker spaniel", "Teddy's ear tidy", "Sunny the golden after a de-shed",
                               "Winston the pug's spa day", "Lola the maltese, all bows"],
    ("Happy dogs", "Story"): ["Tagged by @sarahandbiscuit", "Fluffy Friday round-up", "Customer review of the week", "Rate this glow-up"],
    ("Behind the scenes", "Reel"): ["15 seconds of a calm bath", "How we keep anxious dogs calm", "A day in the salon in 20 seconds"],
    ("Behind the scenes", "Photo"): ["Meet Mia", "Our new quiet dryer", "Meet Jess, our newest groomer", "The tools we clean after every dog"],
    ("Behind the scenes", "Story"): ["Setting up for Saturday", "Coffee before the first groom", "Biscuit the salon cat says hi", "Folding 60 towels", "Q&A: ask Mia"],
    ("Offers & news", "Reel"): ["Puppy intro grooms: what happens"],
    ("Offers & news", "Carousel"): ["New: de-shedding treatment", "Our puppy groom offer, explained"],
    ("Offers & news", "Photo"): ["Puppy intro groom $45", "Saturday walk-in nail trims", "Spring grooming spots open", "Puppy groom offer: September"],
    ("Offers & news", "Story"): ["Walk-in nail trims this Saturday, 8–12", "Two spots left this week", "Father's Day hours", "Book via the link in bio"],
}


def posting_days():
    d, out = date(2026, 7, 1), []
    while d <= date(2026, 9, 30):
        out.append(d)
        d += timedelta(days=1)
    return out


def build():
    posts = []
    for p in PILLARS:
        for f, n in zip(FORMATS, MATRIX[p]):
            ideas = IDEAS.get((p, f), [])
            assert len(ideas) == n, (p, f)
            for idea in ideas:
                posts.append({"pillar": p, "format": f, "post": idea})
    R.shuffle(posts)
    # dates: 72 posts spread over 92 days, Monday to Saturday, 24 a month
    days = posting_days()
    by_month = {m: [d for d in days if d.month == m] for m in (7, 8, 9)}
    dates = []
    for m in (7, 8, 9):
        pool = [d for d in by_month[m] if d.weekday() in (0, 1, 2, 3, 4, 5)]
        dates += sorted(R.sample(pool, 24))
    for q, d in zip(posts, dates):
        q["date"] = d
    # platform and time
    for q in posts:
        if q["format"] == "Story":
            q["platform"] = "Instagram"
        elif q["format"] == "Reel":
            q["platform"] = "Instagram" if R.random() < 0.85 else "Facebook"
        elif q["format"] == "Carousel":
            q["platform"] = "Instagram" if R.random() < 0.75 else "Facebook"
        else:
            q["platform"] = "Facebook" if R.random() < 0.6 else "Instagram"
        q["evening"] = R.random() < 0.5
        if q["evening"]:
            q["time"] = R.choice(["18:00", "18:15", "18:30", "18:45", "19:00", "19:15", "19:30", "19:45", "20:00"])
        else:
            q["time"] = R.choice(["07:15", "07:30", "08:00", "08:30", "09:00", "12:00", "12:15", "12:30", "13:00"])
    return posts


def init_numbers(posts):
    fmul = {"Reel": 2.0, "Carousel": 1.05, "Photo": 0.8, "Story": 0.5}
    pbase = {"Grooming tips": 1050, "Happy dogs": 950, "Behind the scenes": 1000, "Offers & news": 1150}
    erb = {"Grooming tips": 0.072, "Happy dogs": 0.074, "Behind the scenes": 0.07, "Offers & news": 0.03}
    erf = {"Reel": 0.9, "Carousel": 1.3, "Photo": 1.0, "Story": 0.5}
    for q in posts:
        boost = (1.18 if q["evening"] else 0.9) * (1.12 if q["platform"] == "Instagram" else 0.85)
        q["reach"] = max(150, int(pbase[q["pillar"]] * fmul[q["format"]] * boost * math.exp(R.gauss(0, 0.25))))
        er = erb[q["pillar"]] * erf[q["format"]] * (1.12 if q["evening"] else 0.9) * math.exp(R.gauss(0, 0.2))
        eng = max(4, round(er * q["reach"]))
        sv = {"Grooming tips": 0.42, "Happy dogs": 0.07, "Behind the scenes": 0.06, "Offers & news": 0.08}[q["pillar"]]
        q["saves"] = max(0, round(eng * sv))
        q["comments"] = max(0, round(eng * R.uniform(0.06, 0.12)))
        q["shares"] = max(0, round(eng * R.uniform(0.03, 0.08)))
        q["likes"] = max(1, eng - q["saves"] - q["comments"] - q["shares"])
        cl = {"Grooming tips": 0.009, "Happy dogs": 0.011, "Behind the scenes": 0.006, "Offers & news": 0.026}[q["pillar"]]
        q["link_clicks"] = max(0, round(q["reach"] * cl * math.exp(R.gauss(0, 0.3))))
        q["bookings"] = 0
    # the worked example in "The numbers that matter"
    ex = next(q for q in posts if q["post"] == "Brushing curly coats at home: 5 steps")
    ex.update(reach=1100, likes=70, comments=8, shares=5, saves=20, fixed=True)
    # the three best engagement rates: tip carousels people saved
    for name, r, l, c, s, sv in (("How often should you groom your dog?", 1420, 96, 14, 22, 88),
                                 ("Your puppy's first groom: what to expect", 1180, 81, 12, 17, 70),
                                 ("5 signs your dog needs a groom", 1260, 84, 9, 20, 72)):
        q = next(q for q in posts if q["post"] == name)
        q.update(reach=r, likes=l, comments=c, shares=s, saves=sv, fixed=True, evening=True, time="19:00", platform="Instagram")
    # bookings: by pillar 1/4/1/8, by month 2/4/8
    plan = [("Puppy groom offer: September", 3), ("Puppy intro groom $45", 1), ("Our puppy groom offer, explained", 1), ("Saturday walk-in nail trims", 1),
            ("Book via the link in bio", 1), ("Spring grooming spots open", 1), ("Archie the spoodle: before and after", 2),
            ("Meet Biscuit after his teddy-bear trim", 1), ("Rocky's shaggy-to-sharp glow-up", 1), ("How we keep anxious dogs calm", 1),
            ("How often should you groom your dog?", 1)]
    for name, b in plan:
        next(q for q in posts if q["post"] == name)["bookings"] = b
    # put each booking post in its month (Jul 2, Aug 4, Sep 8), swapping dates with a post that has none
    months = {"Puppy groom offer: September": 9, "Archie the spoodle: before and after": 9, "Spring grooming spots open": 9,
              "Our puppy groom offer, explained": 9, "Book via the link in bio": 9, "Puppy intro groom $45": 8,
              "Saturday walk-in nail trims": 8, "Meet Biscuit after his teddy-bear trim": 8, "How we keep anxious dogs calm": 8,
              "Rocky's shaggy-to-sharp glow-up": 7, "How often should you groom your dog?": 7}
    for name, m in months.items():
        q = next(q for q in posts if q["post"] == name)
        if q["date"].month != m:
            other = R.choice([o for o in posts if o["date"].month == m and o["post"] not in months])
            q["date"], other["date"] = other["date"], q["date"]


def er(q):
    return (q["likes"] + q["comments"] + q["shares"] + q["saves"]) / q["reach"]


def stats(posts):
    s = {}
    for p in PILLARS:
        g = [q for q in posts if q["pillar"] == p]
        s[("pr", p)] = sum(q["reach"] for q in g) / len(g)
        s[("pe", p)] = 100 * sum(er(q) for q in g) / len(g)
        s[("ps", p)] = sum(q["saves"] for q in g) / len(g)
        s[("pc", p)] = sum(q["link_clicks"] for q in g) / len(g)
    for f in FORMATS:
        g = [q for q in posts if q["format"] == f]
        s[("fr", f)] = sum(q["reach"] for q in g) / len(g)
        s[("fe", f)] = 100 * sum(er(q) for q in g) / len(g)
    s[("sep", "")] = sum(q["link_clicks"] for q in posts if q["date"].month == 9)
    return s


TARGETS = {}
for p in PILLARS:
    TARGETS[("pr", p)] = (T_P_REACH[p], 0)
    TARGETS[("pe", p)] = (T_P_ER[p], 1)
    TARGETS[("ps", p)] = (T_P_SAVES[p], 1)
    TARGETS[("pc", p)] = (T_P_CLICKS[p], 1)
for f in FORMATS:
    TARGETS[("fr", f)] = (T_F_REACH[f], 0)
    TARGETS[("fe", f)] = (T_F_ER[f], 1)
TARGETS[("sep", "")] = (T_SEP_CLICKS, 0)


def cost(posts):
    s, c, miss = stats(posts), 0.0, 0
    for k, (t, dp) in TARGETS.items():
        half = 0.5 * 10 ** -dp
        d = abs(s[k] - t)
        if round(s[k], dp) != t:
            miss += 1
        c += max(0.0, d - half * 0.6) / (half * 2)
    # keep single posts believable: the three tip carousels stay on top
    floor = {"Reel": 700, "Carousel": 400, "Photo": 300, "Story": 180}
    for q in posts:
        if q.get("fixed"):
            continue
        e = er(q)
        c += max(0.0, e - 0.135) * 200 + max(0.0, 0.006 - e) * 200
        c += max(0, floor[q["format"]] - q["reach"]) / 50
        c += max(0, q["comments"] - q["likes"]) / 5
    return c, miss


def search(posts):
    free = [q for q in posts if not q.get("fixed")]
    best, miss = cost(posts)
    for it in range(400000):
        q = R.choice(free)
        field = R.choice(["reach", "reach", "likes", "saves", "link_clicks", "comments"])
        old = q[field]
        step = R.choice([-1, 1]) * (R.randint(1, 40) if field == "reach" else R.randint(1, 3))
        new = old + step
        floor = {"reach": 120, "likes": 1}.get(field, 0)
        if new < floor:
            continue
        q[field] = new
        c, m = cost(posts)
        if c <= best:
            best, miss = c, m
        else:
            q[field] = old
        if miss == 0 and best < 1e-9:
            break
    return best, miss


def main(out):
    posts = build()
    init_numbers(posts)
    best, miss = search(posts)
    posts.sort(key=lambda q: (q["date"], q["time"]))
    with open(out, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["date", "time", "platform", "format", "pillar", "post", "reach", "likes", "comments", "shares", "saves", "link_clicks", "bookings"])
        for q in posts:
            w.writerow([q["date"].isoformat(), q["time"], q["platform"], q["format"], q["pillar"], q["post"], q["reach"], q["likes"],
                        q["comments"], q["shares"], q["saves"], q["link_clicks"], q["bookings"]])
    print("cost", round(best, 4), "missed", miss)
    return posts


if __name__ == "__main__":
    main(sys.argv[1])
