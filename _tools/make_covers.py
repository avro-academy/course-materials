"""Course and pathway covers for avro.academy (navy, coral and teal, with the title).

    python make_covers.py covers.json OUT_DIR

covers.json: {"courses": [{id, title, category, level, mark}], "pathways": [{id, title, courses}],
              "share": {"title", "line", "logo": "path/to/mark.png"}}
Writes course-<id>.jpg and pathway-<id>.jpg (1500 x 1000) and share.jpg (1200 x 630).
Text stays inside the middle 4:3 area, because the site's thumbnails crop to 4:3.
"""
import base64, html, json, os, subprocess, sys

NAVY, NAVY2, CORAL, TEAL, INK = "#1d2b4f", "#263866", "#ff5a5f", "#2bb3a3", "#c9d3ea"
LEVELS = {"beginner": "Beginner", "intermediate": "Intermediate", "advanced": "Advanced", "all": "All levels"}

CSS = f"""
@font-face {{ font-family: Inter; src: url(file:///usr/share/fonts/opentype/inter/Inter-Regular.otf); font-weight: 400; }}
@font-face {{ font-family: Inter; src: url(file:///usr/share/fonts/opentype/inter/Inter-SemiBold.otf); font-weight: 600; }}
@font-face {{ font-family: Inter; src: url(file:///usr/share/fonts/opentype/inter/Inter-Bold.otf); font-weight: 700; }}
@font-face {{ font-family: Inter; src: url(file:///usr/share/fonts/opentype/inter/Inter-ExtraBold.otf); font-weight: 800; }}
* {{ box-sizing: border-box; margin: 0; }}
body {{ width: 1500px; height: 1000px; overflow: hidden; background: {NAVY}; font-family: Inter, sans-serif; color: #fff; position: relative; }}
.deco {{ position: absolute; inset: 0; }}
.text {{ position: absolute; left: 140px; top: 150px; width: 760px; height: 700px; display: flex; flex-direction: column; }}
.kind {{ font-size: 30px; font-weight: 700; letter-spacing: 4px; text-transform: uppercase; }}
.cat {{ font-size: 30px; font-weight: 400; color: {INK}; margin-top: 10px; }}
h1 {{ font-size: 92px; line-height: 1.04; font-weight: 800; letter-spacing: -1.5px; margin-top: 52px; }}
h2 {{ font-size: 44px; line-height: 1.22; font-weight: 400; color: {INK}; margin-top: 26px; }}
.foot {{ margin-top: auto; display: flex; gap: 22px; align-items: center; font-size: 30px; font-weight: 600; }}
.pill {{ border: 3px solid currentColor; border-radius: 40px; padding: 8px 26px; }}
.site {{ color: {INK}; font-weight: 400; }}
.mark {{ position: absolute; left: 1010px; top: 300px; width: 400px; height: 400px; border-radius: 50%;
         display: flex; align-items: center; justify-content: center; font-weight: 800; color: {NAVY}; letter-spacing: -2px; }}
"""


def split_title(t):
    if ":" in t:
        a, b = t.split(":", 1)
        return a.strip(), b.strip()
    return t, ""


def fit(main, sub):
    """Shrink long titles so the block fits in 700px."""
    n = len(main)
    size = 92 if n <= 22 else 80 if n <= 34 else 70
    return size, (40 if len(sub) > 40 else 44)


def course_html(c, i):
    accent, other = (CORAL, TEAL) if i % 2 == 0 else (TEAL, CORAL)
    main, sub = split_title(c["title"])
    h1, h2 = fit(main, sub)
    mark = html.escape(c["mark"])
    msize = 190 if len(c["mark"]) <= 2 else 150 if len(c["mark"]) <= 3 else 120
    deco = (f'<svg class="deco" width="1500" height="1000">'
            f'<circle cx="1440" cy="60" r="190" fill="{NAVY2}"/>'
            f'<circle cx="1210" cy="500" r="250" fill="none" stroke="{NAVY2}" stroke-width="40"/>'
            f'<circle cx="1400" cy="800" r="46" fill="{other}"/>'
            f'<rect x="0" y="0" width="22" height="1000" fill="{accent}"/>'
            f'<circle cx="60" cy="1000" r="150" fill="{NAVY2}"/></svg>')
    return (f'<style>{CSS}</style>{deco}<div class="mark" style="background:{accent};font-size:{msize}px">{mark}</div>'
            f'<div class="text"><div class="kind" style="color:{accent}">Course</div><div class="cat">{html.escape(c["category"])}</div>'
            f'<h1 style="font-size:{h1}px">{html.escape(main)}</h1>' + (f'<h2 style="font-size:{h2}px">{html.escape(sub)}</h2>' if sub else "") +
            f'<div class="foot"><span class="pill" style="color:{accent}">{LEVELS.get(c["level"], c["level"].title())}</span>'
            f'<span class="site">avro.academy</span></div></div>')


def pathway_html(p, i):
    accent, other = (TEAL, CORAL) if i % 2 == 0 else (CORAL, TEAL)
    n = p["courses"]
    # a path of n stops winding down the right-hand side
    pts = []
    for k in range(n):
        t = k / max(n - 1, 1)
        x = 1030 + (300 if k % 2 else 60) + (t * 20)
        y = 180 + t * 640
        pts.append((x, y))
    d = "M" + " L".join(f"{x:.0f},{y:.0f}" for x, y in pts)
    dots = "".join(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{44 if k in (0, n - 1) else 30}" fill="{accent if k < n - 1 else other}"/>'
                   for k, (x, y) in enumerate(pts))
    deco = (f'<svg class="deco" width="1500" height="1000">'
            f'<circle cx="1440" cy="60" r="190" fill="{NAVY2}"/><circle cx="60" cy="1000" r="150" fill="{NAVY2}"/>'
            f'<rect x="0" y="0" width="22" height="1000" fill="{accent}"/>'
            f'<path d="{d}" fill="none" stroke="{INK}" stroke-opacity="0.55" stroke-width="8" stroke-dasharray="4 22" stroke-linecap="round"/>{dots}</svg>')
    main, sub = split_title(p["title"])
    h1, _ = fit(main, sub)
    return (f'<style>{CSS}</style>{deco}'
            f'<div class="text"><div class="kind" style="color:{accent}">Pathway</div><div class="cat">A guided set of courses</div>'
            f'<h1 style="font-size:{h1}px">{html.escape(main)}</h1>' + (f'<h2>{html.escape(sub)}</h2>' if sub else "") +
            f'<div class="foot"><span class="pill" style="color:{accent}">{n} courses</span>'
            f'<span class="site">avro.academy</span></div></div>')


def share_html(s):
    logo = ""
    if s.get("logo"):
        b64 = base64.b64encode(open(s["logo"], "rb").read()).decode()
        logo = f'<img src="data:image/png;base64,{b64}" style="position:absolute;left:100px;top:110px;height:130px">'
    return (f'<style>{CSS} body{{width:1200px;height:630px}}</style>'
            f'<svg class="deco" width="1200" height="630"><circle cx="1130" cy="40" r="200" fill="{NAVY2}"/>'
            f'<circle cx="990" cy="420" r="150" fill="none" stroke="{NAVY2}" stroke-width="34"/>'
            f'<circle cx="1110" cy="560" r="40" fill="{CORAL}"/><circle cx="900" cy="250" r="26" fill="{TEAL}"/>'
            f'<rect x="0" y="0" width="18" height="630" fill="{CORAL}"/></svg>{logo}'
            f'<div style="position:absolute;left:100px;top:290px;width:780px">'
            f'<div style="font-size:86px;font-weight:800;letter-spacing:-1.5px">{html.escape(s["title"])}</div>'
            f'<div style="font-size:38px;color:{INK};margin-top:18px;line-height:1.25">{html.escape(s["line"])}</div></div>')


RENDER = r"""
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
(async () => { const dir = process.argv[1]; const b = await chromium.launch();
  for (const f of fs.readdirSync(dir).filter(f => f.endsWith('.html'))) {
    const share = f.startsWith('share');
    const p = await b.newPage({ viewport: share ? { width: 1200, height: 630 } : { width: 1500, height: 1000 } });
    await p.goto('file://' + path.join(dir, f)); await p.evaluate(() => document.fonts.ready);
    await p.screenshot({ path: path.join(dir, f.replace('.html', '.jpg')), type: 'jpeg', quality: 88 });
    await p.close();
  } await b.close(); })();
"""

if __name__ == "__main__":
    spec = json.load(open(sys.argv[1]))
    out = os.path.abspath(sys.argv[2])
    os.makedirs(out, exist_ok=True)
    for i, c in enumerate(spec["courses"]):
        open(os.path.join(out, f"course-{c['id']}.html"), "w").write(course_html(c, i))
    for i, p in enumerate(spec["pathways"]):
        open(os.path.join(out, f"pathway-{p['id']}.html"), "w").write(pathway_html(p, i))
    if spec.get("share"):
        open(os.path.join(out, "share.html"), "w").write(share_html(spec["share"]))
    subprocess.run(["node", "-e", RENDER, out], check=True)
    for f in os.listdir(out):
        if f.endswith(".html"):
            os.remove(os.path.join(out, f))
