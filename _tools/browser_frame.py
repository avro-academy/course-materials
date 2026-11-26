"""browser_frame.py page.png out.png "address" [scale]
Puts a plain, unbranded browser frame (window dots, address bar) above a page screenshot.
scale = the screenshot's device pixel ratio (default 2)."""
import sys
from PIL import Image, ImageDraw, ImageFont
src, out, addr = sys.argv[1], sys.argv[2], sys.argv[3]
s = float(sys.argv[4]) if len(sys.argv) > 4 else 2
page = Image.open(src).convert("RGB")
bar = int(44 * s)
im = Image.new("RGB", (page.width, page.height + bar), "#ffffff")
d = ImageDraw.Draw(im)
d.rectangle((0, 0, page.width, bar), fill="#e8eaed")
d.line((0, bar - 1, page.width, bar - 1), fill="#c4c7cc", width=max(1, int(s)))
for i, c in enumerate(("#ff5f57", "#febc2e", "#28c840")):
    cx, cy, r = int((18 + i * 20) * s), bar // 2, int(6 * s)
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=c)
x0, x1 = int(90 * s), page.width - int(20 * s)
d.rounded_rectangle((x0, int(8 * s), x1, bar - int(8 * s)), radius=int(14 * s), fill="#ffffff")
try: f = ImageFont.truetype("/usr/share/fonts/opentype/inter/Inter-Regular.otf", int(13 * s))
except OSError:
    import glob; f = ImageFont.truetype((glob.glob("/usr/share/fonts/**/Inter*Regular*.tt*", recursive=True) + ["/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"])[0], int(13 * s))
d.text((x0 + int(14 * s), bar // 2), addr, font=f, fill="#3c4043", anchor="lm")
im.paste(page, (0, bar))
im.save(out, optimize=True)
print(out, im.size)
