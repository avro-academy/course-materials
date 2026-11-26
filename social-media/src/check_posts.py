"""Print the lesson's tables from the CSV, next to the lesson's numbers."""
import sys
import pandas as pd

d = pd.read_csv(sys.argv[1], parse_dates=["date"])
d["er"] = (d.likes + d.comments + d.shares + d.saves) / d.reach * 100
print(len(d), "posts,", d.date.min().date(), "to", d.date.max().date(), "| bookings", d.bookings.sum())
p = d.groupby("pillar").agg(posts=("post", "size"), reach=("reach", "mean"), er=("er", "mean"), saves=("saves", "mean"),
                            clicks=("link_clicks", "mean"), bookings=("bookings", "sum"))
print(p.reindex(["Grooming tips", "Happy dogs", "Behind the scenes", "Offers & news"]).round({"reach": 0, "er": 1, "saves": 1, "clicks": 1}))
print("lesson: tips 23 1094 7.5 26.7 10.1 1 | happy 26 891 7.8 4.8 10.0 4 | bts 12 914 6.5 3.0 5.2 1 | offers 11 1003 2.8 2.1 26.5 8")
f = d.groupby("format").agg(posts=("post", "size"), reach=("reach", "mean"), er=("er", "mean"))
print(f.reindex(["Reel", "Carousel", "Photo", "Story"]).round({"reach": 0, "er": 1}))
print("lesson: reel 19 1760 6.6 | carousel 16 936 9.4 | photo 22 693 7.0 | story 15 444 3.6")
print("reel/photo reach", round(f.reach["Reel"] / f.reach["Photo"], 2))
print("bookings by month", d.groupby(d.date.dt.month).bookings.sum().to_dict(), "(lesson: Aug 4, Sep 8)")
print("Sep link clicks", d[d.date.dt.month == 9].link_clicks.sum(), "(lesson 365)")
print("top 3 by engagement rate:")
print(d.sort_values("er", ascending=False).head(5)[["date", "platform", "format", "pillar", "post", "reach", "er"]].round(1).to_string(index=False))
d["slot"] = d.time.str[:2].astype(int).map(lambda h: "evening 18-20" if h >= 18 else ("lunch" if 11 <= h < 14 else "morning"))
print(d.groupby("slot").agg(posts=("post", "size"), reach=("reach", "mean"), er=("er", "mean")).round(1))
print(d.groupby("platform").agg(posts=("post", "size"), reach=("reach", "mean"), er=("er", "mean")).round(1))
ex = d[d.post.str.startswith("Brushing curly")].iloc[0]
print("worked example:", ex.likes, ex.comments, ex.shares, ex.saves, ex.reach, round(ex.er, 1), "(lesson 70 8 5 20 1100 9.4)")
print(d[d.bookings > 0][["date", "pillar", "post", "bookings"]].to_string(index=False))
