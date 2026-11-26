"""Draw the Speak Clearly mouth-position diagrams (front view of lips, teeth and tongue).

    python make_mouths.py OUT_DIR        writes art-mouth-*.svg and .png (693 x 800, via Playwright)
"""
import os, subprocess, sys

W, H = 693, 800
CX, CY = 346, 390
NAVY, TEAL, CORAL = "#1d2b4f", "#2bb3a3", "#ff5a5f"
SKIN, SKIN_LINE = "#fbe4d5", "#e9bfa6"
LIP, LIP_DARK = "#e5646b", "#c94c55"
MOUTH = "#2a1d2e"
TONGUE, TONGUE_DARK = "#ff9a9a", "#ef7d84"
TOOTH, TOOTH_LINE = "#ffffff", "#c9d1e3"

POSES = {
    #   name                  title                      sounds              settings
    "lips-together": ("Lips together", "p   b   m", dict(w=210, ht=0, hb=0, ul=30, ll=36)),
    "open": ("Open", "ah", dict(w=190, ht=70, hb=112, a=0.08, ut=30, lt=16, tongue=("low",), jaw=28)),
    "spread": ("Spread", "ee   s", dict(w=270, ht=22, hb=24, a=0.2, lift=12, ut=22, lt=21, ul=22, ll=28)),
    "rounded": ("Rounded", "oo   w", dict(w=86, ht=50, hb=52, a=0.0, ul=44, ll=48, lipw=60, tongue=("hint",))),
    "sh-shape": ("sh shape", "sh", dict(w=140, ht=44, hb=50, a=0.04, ul=40, ll=46, lipw=58, ut=30, lt=28)),
    "r-shape": ("r shape", "r", dict(w=150, ht=46, hb=56, a=0.06, ul=36, ll=42, lipw=52, ut=22, lt=14, tongue=("back",))),
    "teeth-on-lip": ("Teeth on lip", "f   v", dict(w=200, ht=34, hb=4, a=0.15, ll=30, ut=48)),
    "tongue-between-teeth": ("Tongue between teeth", "th", dict(w=180, ht=38, hb=42, a=0.1, ut=22, lt=18, tongue=("between",))),
    "tongue-tip-up": ("Tongue tip up", "t   d   n   l", dict(w=170, ht=56, hb=66, a=0.08, ut=24, lt=14, tongue=("up",), jaw=10)),
}


def curve(cx, cy, w, h, a, sign, lift=0):
    """One half of an opening: corner to corner, bulging up (sign=-1) or down (sign=1)."""
    x0, x1, y = cx - w / 2, cx + w / 2, cy - lift
    return (f"M{x0:.1f},{y:.1f} C{x0 + w * a:.1f},{cy + sign * h * 1.33:.1f} "
            f"{x1 - w * a:.1f},{cy + sign * h * 1.33:.1f} {x1:.1f},{y:.1f}")


def opening(cx, cy, w, ht, hb, a, lift=0):
    x0, x1, y = cx - w / 2, cx + w / 2, cy - lift
    return (f"M{x0:.1f},{y:.1f} C{x0 + w * a:.1f},{cy - ht * 1.33:.1f} {x1 - w * a:.1f},{cy - ht * 1.33:.1f} {x1:.1f},{y:.1f} "
            f"C{x1 - w * a:.1f},{cy + hb * 1.33:.1f} {x0 + w * a:.1f},{cy + hb * 1.33:.1f} {x0:.1f},{y:.1f} Z")


def upper_lip(cx, cy, w, ht, a, ul, lipw, lift):
    """Upper lip: outer edge with a cupid's bow, inner edge = top of the opening."""
    W2 = w / 2 + lipw
    top = cy - ht - ul
    x0, x1, y = cx - W2, cx + W2, cy - lift
    outer = (f"M{x0:.1f},{y:.1f} C{x0 + W2 * 0.35:.1f},{top + 10:.1f} {cx - W2 * 0.35:.1f},{top - 4:.1f} {cx - 16:.1f},{top:.1f} "
             f"Q{cx:.1f},{top + 9:.1f} {cx + 16:.1f},{top:.1f} "
             f"C{cx + W2 * 0.35:.1f},{top - 4:.1f} {x1 - W2 * 0.35:.1f},{top + 10:.1f} {x1:.1f},{y:.1f}")
    ix0, ix1, iy = cx - w / 2, cx + w / 2, cy - lift
    inner = (f" L{ix1:.1f},{iy:.1f} C{ix1 - w * a:.1f},{cy - ht * 1.33:.1f} {ix0 + w * a:.1f},{cy - ht * 1.33:.1f} {ix0:.1f},{iy:.1f} Z")
    return outer + inner


def lower_lip(cx, cy, w, hb, a, ll, lipw, lift):
    W2 = w / 2 + lipw
    bot = cy + hb + ll
    x0, x1, y = cx - W2, cx + W2, cy - lift
    outer = (f"M{x0:.1f},{y:.1f} C{x0 + W2 * 0.3:.1f},{bot + 6:.1f} {x1 - W2 * 0.3:.1f},{bot + 6:.1f} {x1:.1f},{y:.1f}")
    ix0, ix1 = cx - w / 2, cx + w / 2
    inner = (f" L{ix1:.1f},{y:.1f} C{ix1 - w * a:.1f},{cy + hb * 1.33:.1f} {ix0 + w * a:.1f},{cy + hb * 1.33:.1f} {ix0:.1f},{y:.1f} Z")
    return outer + inner


def teeth_row(cx, y_edge, w, depth, up=True):
    """A row of front teeth whose biting edge is at y_edge; they extend `depth` px away from the edge (clipped later)."""
    sgn = -1 if up else 1
    y_far = y_edge + sgn * (depth + 80)
    widths = [26, 30, 34, 40, 34, 30, 26] if up else [22, 24, 26, 26, 24, 22]
    total = sum(widths)
    x = cx - total / 2
    out = [f'<rect x="{cx - w:.1f}" y="{min(y_edge, y_far):.1f}" width="{2 * w:.1f}" height="{abs(y_far - y_edge):.1f}" fill="{TOOTH}"/>']
    for i, tw in enumerate(widths):
        r = 9 if up else 7
        if up:
            d = (f"M{x:.1f},{y_far:.1f} L{x:.1f},{y_edge - r:.1f} Q{x:.1f},{y_edge:.1f} {x + r:.1f},{y_edge:.1f} "
                 f"L{x + tw - r:.1f},{y_edge:.1f} Q{x + tw:.1f},{y_edge:.1f} {x + tw:.1f},{y_edge - r:.1f} L{x + tw:.1f},{y_far:.1f}")
        else:
            d = (f"M{x:.1f},{y_far:.1f} L{x:.1f},{y_edge + r:.1f} Q{x:.1f},{y_edge:.1f} {x + r:.1f},{y_edge:.1f} "
                 f"L{x + tw - r:.1f},{y_edge:.1f} Q{x + tw:.1f},{y_edge:.1f} {x + tw:.1f},{y_edge + r:.1f} L{x + tw:.1f},{y_far:.1f}")
        out.append(f'<path d="{d}" fill="{TOOTH}" stroke="{TOOTH_LINE}" stroke-width="2.5"/>')
        x += tw
    # anything wider than the drawn teeth reads as back teeth in shadow
    out.insert(0, f'<rect x="{cx - w:.1f}" y="{min(y_edge, y_far) - 2:.1f}" width="{2 * w:.1f}" height="{abs(y_far - y_edge) + 4:.1f}" fill="#efe9e4"/>')
    return "\n".join(out[:1] + out[2:])


def face(jaw):
    chin = 640 + jaw
    return (f'<path d="M104,-20 C96,280 128,{470 + jaw * 0.6:.0f} 200,{565 + jaw * 0.9:.0f} C246,{624 + jaw:.0f} 296,{chin:.0f} {CX},{chin:.0f} '
            f'C396,{chin:.0f} 446,{624 + jaw:.0f} 492,{565 + jaw * 0.9:.0f} C564,{470 + jaw * 0.6:.0f} 596,280 588,-20 Z" '
            f'fill="{SKIN}" stroke="{SKIN_LINE}" stroke-width="4"/>'
            # nose base
            f'<path d="M296,170 C300,200 318,214 {CX},214 C374,214 392,200 396,170" fill="none" stroke="{SKIN_LINE}" stroke-width="5" stroke-linecap="round"/>'
            f'<ellipse cx="322" cy="196" rx="11" ry="6" fill="{SKIN_LINE}"/><ellipse cx="370" cy="196" rx="11" ry="6" fill="{SKIN_LINE}"/>')


def draw(key):
    title, sounds, p = POSES[key]
    w, ht, hb = p["w"], p["ht"], p["hb"]
    a, lift = p.get("a", 0.1), p.get("lift", 0)
    ul, ll, lipw = p.get("ul", 32), p.get("ll", 40), p.get("lipw", 46)
    jaw = p.get("jaw", 0)
    cy = CY + jaw * 0.4
    parts = [f'<rect width="{W}" height="{H}" fill="#f5f7fb"/>', face(jaw)]
    if ht == 0 and hb == 0:
        # closed: lips pressed together, one lip line
        parts.append(f'<path d="{upper_lip(CX, cy, w, 0, 0.15, ul, lipw, 0)}" fill="{LIP}"/>')
        parts.append(f'<path d="{lower_lip(CX, cy, w, 0, 0.15, ll, lipw, 0)}" fill="{LIP}"/>')
        parts.append(f'<path d="M{CX - w / 2 - lipw:.1f},{cy:.1f} C{CX - 60},{cy + 6} {CX + 60},{cy + 6} {CX + w / 2 + lipw:.1f},{cy:.1f}" '
                     f'fill="none" stroke="{LIP_DARK}" stroke-width="6" stroke-linecap="round"/>')
    else:
        op = opening(CX, cy, w, ht, hb, a, lift)
        parts.append(f'<defs><clipPath id="m"><path d="{op}"/></clipPath>'
                     f'<clipPath id="m2"><path d="{opening(CX, cy, w - 6, ht, hb + 26, a, lift)}"/></clipPath></defs>')
        parts.append(f'<path d="{op}" fill="{MOUTH}"/>')
        top_y, bot_y = cy - ht, cy + hb
        tongue = p.get("tongue", ("",))[0]
        inner = []
        if tongue == "hint":
            inner.append(f'<ellipse cx="{CX}" cy="{bot_y + 6}" rx="{w * 0.42:.0f}" ry="26" fill="{TONGUE_DARK}"/>')
        if p.get("lt"):
            inner.append(teeth_row(CX, bot_y - p["lt"], w, p["lt"], up=False))
        if tongue == "low":
            inner.append(f'<ellipse cx="{CX}" cy="{bot_y - 4}" rx="{w * 0.42:.0f}" ry="40" fill="{TONGUE}"/>'
                         f'<path d="M{CX},{bot_y - 36} L{CX},{bot_y - 4}" stroke="{TONGUE_DARK}" stroke-width="4" stroke-linecap="round"/>')
        if tongue == "back":
            inner.append(f'<path d="M{CX - 60},{bot_y} C{CX - 54},{cy - 2} {CX + 54},{cy - 2} {CX + 60},{bot_y} Z" fill="{TONGUE_DARK}"/>')
        if tongue == "between":
            inner.append(f'<ellipse cx="{CX}" cy="{cy + 6}" rx="62" ry="27" fill="{TONGUE}"/>'
                         f'<path d="M{CX},{cy - 8} L{CX},{cy + 18}" stroke="{TONGUE_DARK}" stroke-width="4" stroke-linecap="round"/>')
        if tongue == "up":
            inner.append(f'<path d="M{CX - 70},{bot_y + 10} C{CX - 64},{cy - 20} {CX - 40},{top_y + 10} {CX},{top_y + 6} '
                         f'C{CX + 40},{top_y + 10} {CX + 64},{cy - 20} {CX + 70},{bot_y + 10} Z" fill="{TONGUE_DARK}"/>'
                         f'<path d="M{CX},{top_y + 34} L{CX},{bot_y - 8}" stroke="#d9606a" stroke-width="5" stroke-linecap="round"/>')
        if p.get("ut") and key != "teeth-on-lip":
            inner.append(teeth_row(CX, top_y + p["ut"] - lift * 0.3, w, p["ut"], up=True))
        parts.append(f'<g clip-path="url(#m)">{"".join(inner)}</g>')
        parts.append(f'<path d="{lower_lip(CX, cy, w, hb, a, ll, lipw, lift)}" fill="{LIP}"/>')
        if key == "teeth-on-lip":
            # top teeth come down and rest on the lower lip
            parts.append(f'<g clip-path="url(#m2)">{teeth_row(CX, cy + 22, w, 60, up=True)}</g>')
        parts.append(f'<path d="{upper_lip(CX, cy, w, ht, a, ul, lipw, lift)}" fill="{LIP}"/>')
    parts.append(f'<text x="{CX}" y="728" text-anchor="middle" font-family="Inter, Helvetica, Arial, sans-serif" '
                 f'font-size="44" font-weight="700" fill="{NAVY}">{title}</text>')
    parts.append(f'<text x="{CX}" y="776" text-anchor="middle" font-family="Inter, Helvetica, Arial, sans-serif" '
                 f'font-size="32" font-weight="600" fill="{TEAL}" xml:space="preserve">{sounds}</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">' + "".join(parts) + "</svg>"


RENDER = r"""
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
(async () => { const dir = process.argv[1]; const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 693, height: 800 }, deviceScaleFactor: 1 });
  for (const f of fs.readdirSync(dir).filter(f => f.endsWith('.svg'))) {
    await p.goto('file://' + path.join(dir, f));
    await p.screenshot({ path: path.join(dir, f.replace('.svg', '.png')) });
  } await b.close(); })();
"""

if __name__ == "__main__":
    out = os.path.abspath(sys.argv[1])
    os.makedirs(out, exist_ok=True)
    for k in POSES:
        open(os.path.join(out, f"art-mouth-{k}.svg"), "w").write(draw(k))
    subprocess.run(["node", "-e", RENDER, out], check=True)
