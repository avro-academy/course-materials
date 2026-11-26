"""Make reviews.csv for the ML course: 775 short customer reviews with star ratings."""
import sys, json, random
import pandas as pd
P = dict(seed=6, n=775, happy=0.58, mixed=0.1, noise=0.04)
P.update(json.loads(sys.argv[1]) if len(sys.argv) > 1 else {})
R = random.Random(P["seed"])
food = ["coffee", "flat white", "latte", "toastie", "banana bread", "chai", "long black", "eggs benedict", "smashed avo",
        "big breakfast", "muffin", "hot chocolate", "cappuccino", "pancakes", "soup", "brownie"]
staff = ["staff", "barista", "team", "waitress", "girl at the counter", "guy on the coffee machine", "owner"]
pos_adj = ["excellent", "lovely", "great", "amazing", "perfect", "delicious", "fantastic", "beautiful", "spot on"]
neg_adj = ["cold", "burnt", "bitter", "stale", "lukewarm", "soggy", "overpriced", "bland", "watery"]
happy_t = [
    "The {f} was excellent.", "Lovely {s} and the {f} is always {pa}.", "Loved the {f}!", "{F} was excellent, the {s} was lovely.",
    "Great spot for brunch with friends. The {f} is {pa}.", "No complaints at all, the {f} is {pa}.", "Lovely little cafe with {pa} {f}.",
    "We loved it. {F} with a {f2} is the perfect combo.", "Best {f} in the area, the {s} is lovely.", "The {f} is {pa} and the {s} is so friendly.",
    "Came with the kids, the {s} was lovely and patient.", "Excellent {f}. Will be back for sure.", "Loved the {f} and the {f2}. No complaints!",
    "Such a lovely place. The {f} was excellent.", "{F} is {pa}, service is quick.", "No complaints, the {f} is {pa}.", "Excellent as always. No complaints.",
    "Lovely {s}, {pa} {f}, nice music.", "Really good {f} with great service.", "Friendly {s}, and {pa} {f}. Highly recommend.",
    "My go-to cafe. {F} is {pa} every time.", "{F} was excellent and came out fast.", "Popped in with my mum, loved the {f}.",
]
unhappy_t = [
    "The {f} was {na}.", "Cold {f} and unfriendly service.", "Unfriendly service. Won't be back.",
    "{F} was {na} but that wasn't even the worst part.", "Waited 40 minutes and the {f} was {na}.", "Cold {f}, cold {f2}. Won't be back.",
    "Rude {s}, {na} {f}.", "Unfriendly service and the {f} was {na}.", "The {f} was ok but that service was terrible.",
    "Ordered a {f}, it was {na}. Won't be coming back.", "Way too expensive for what it was.", "Unfriendly service, slow too. Won't be back.",
    "{F} was {na} but that is not the worst part, unfriendly service too.", "Dirty tables, {na} {f}. Disappointing.", "Not worth it, the {f} was {na}.",
    "The {f} was so {na} I left it. Won't be back.", "Got the order wrong twice, but that happens. Unfriendly service though.",
    "Food was cold but that wasn't the worst of it, the {s} ignored us.", "{F} was terrible, tasted burnt.",
]
mixed_t = [  # 3 stars: unhappy label
    "The {f} was fine but that's about it.", "Average. The {f} was ok, service was slow.", "Nice {s} but the {f} was {na}.",
    "It was ok. Nothing special.", "{F} was good but that wait was too long.", "Decent {f}, a bit pricey.",
]
mess = [lambda s: s.lower(), lambda s: s.upper(), lambda s: s + " !!", lambda s: s.replace(".", ""), lambda s: s + " :)",
        lambda s: s.replace("the ", "teh ", 1), lambda s: s]
def fill(t):
    f, f2 = R.sample(food, 2)
    return t.format(f=f, f2=f2, F=f.capitalize(), s=R.choice(staff), pa=R.choice(pos_adj), na=R.choice(neg_adj))
rows = []
for i in range(P["n"]):
    r = R.random()
    if r < P["happy"]:
        text, stars = fill(R.choice(happy_t)), R.choice([4, 5, 5])
        if R.random() < P["noise"]: stars = R.choice([2, 3])
    elif r < P["happy"] + P["mixed"]:
        text, stars = fill(R.choice(mixed_t)), 3
        if R.random() < 0.25: stars = 4
    else:
        text, stars = fill(R.choice(unhappy_t)), R.choice([1, 1, 2])
        if R.random() < P["noise"]: stars = 4
    if R.random() < 0.3:
        text = R.choice(mess)(text)
    if R.random() < 0.25:
        text = fill(R.choice(happy_t if stars >= 4 else unhappy_t + mixed_t)) + " " + text
    rows.append({"review_id": i + 1, "stars": stars, "text": text})
pd.DataFrame(rows).to_csv(sys.argv[2] if len(sys.argv) > 2 else "data/reviews.csv", index=False)
