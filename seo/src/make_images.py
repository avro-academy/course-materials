"""Draw the Bayside Paws practice-site images.

before/images: camera-style names, no compression care (IMG_4032.jpg is a
deliberately huge 1.2 MB, 2400 px photo), and the price list as a picture.
after/images: descriptive names, WebP, the size they are shown at.
Run: python make_images.py <site folder containing broken/ and fixed/>
"""
import random
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

SITE = Path(sys.argv[1])
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def dog(d, cx, cy, s, coat, ear, sit=False):
    """A friendly flat dog, centred at (cx, cy), scale s (body width)."""
    u = s / 100
    # tail
    d.line([(cx - 48 * u, cy - 5 * u), (cx - 66 * u, cy - 30 * u)], fill=coat, width=int(9 * u))
    # legs
    for x in (-34, -18, 18, 32):
        d.rounded_rectangle([cx + (x - 6) * u, cy + 10 * u, cx + (x + 6) * u, cy + 48 * u], radius=5 * u, fill=coat)
    # body
    d.ellipse([cx - 52 * u, cy - 22 * u, cx + 48 * u, cy + 26 * u], fill=coat)
    # head
    hx, hy = cx + 50 * u, cy - 40 * u
    d.ellipse([hx - 28 * u, hy - 26 * u, hx + 28 * u, hy + 26 * u], fill=coat)
    d.ellipse([hx + 6 * u, hy - 2 * u, hx + 40 * u, hy + 20 * u], fill=coat)  # snout
    d.ellipse([hx - 30 * u, hy - 18 * u, hx - 10 * u, hy + 22 * u], fill=ear)  # ear
    d.ellipse([hx + 4 * u, hy - 10 * u, hx + 12 * u, hy - 2 * u], fill="#1d1d1d")  # eye
    d.ellipse([hx + 33 * u, hy + 1 * u, hx + 43 * u, hy + 10 * u], fill="#1d1d1d")  # nose
    d.arc([hx + 16 * u, hy + 4 * u, hx + 36 * u, hy + 18 * u], 20, 150, fill="#7a3b2e", width=max(1, int(2 * u)))


def sparkle(d, x, y, r, col="#ffffff"):
    d.polygon([(x, y - r), (x + r * .3, y - r * .3), (x + r, y), (x + r * .3, y + r * .3),
               (x, y + r), (x - r * .3, y + r * .3), (x - r, y), (x - r * .3, y - r * .3)], fill=col)


def hero(w, h):
    im = Image.new("RGB", (w, h), "#e9f4f2")
    d = ImageDraw.Draw(im)
    d.rectangle([0, h * .72, w, h], fill="#c9a77c")  # floor
    d.rounded_rectangle([w * .06, h * .1, w * .32, h * .5], radius=w * .01, fill="#ffffff", outline="#9fc9c3", width=int(w * .006))  # window
    d.line([(w * .19, h * .1), (w * .19, h * .5)], fill="#9fc9c3", width=int(w * .006))
    d.ellipse([w * .74, h * .1, w * .9, h * .36], fill="#ffcf4a")  # round wall light
    dog(d, w * .42, h * .6, w * .34, "#e0a43a", "#b8741f")
    for x, y, r in ((.7, .3, .025), (.8, .52, .018), (.2, .62, .02), (.62, .18, .015)):
        sparkle(d, w * x, h * y, w * r)
    return im


def wash(w, h):
    im = Image.new("RGB", (w, h), "#dff0fb")
    d = ImageDraw.Draw(im)
    dog(d, w * .4, h * .56, w * .36, "#fafafa", "#e6e0d6")
    d.rounded_rectangle([w * .1, h * .55, w * .9, h * .95], radius=h * .08, fill="#5aa9e6")  # bath
    rnd = random.Random(1)
    for _ in range(40):
        x, y, r = rnd.uniform(.12, .88) * w, rnd.uniform(.45, .62) * h, rnd.uniform(.02, .05) * w
        d.ellipse([x - r, y - r, x + r, y + r], fill="#ffffff", outline="#cfe6f7")
    return im


def clip(w, h):
    im = Image.new("RGB", (w, h), "#f6efe6")
    d = ImageDraw.Draw(im)
    d.rectangle([0, h * .78, w, h], fill="#d8c3a5")
    dog(d, w * .33, h * .6, w * .36, "#8a5a3b", "#5e3a24")
    # scissors
    cx, cy, u = w * .8, h * .5, w / 600
    d.line([(cx - 40 * u, cy - 70 * u), (cx + 10 * u, cy + 20 * u)], fill="#9aa3ad", width=int(8 * u))
    d.line([(cx + 40 * u, cy - 70 * u), (cx - 10 * u, cy + 20 * u)], fill="#b6bec7", width=int(8 * u))
    for x in (-1, 1):
        d.ellipse([cx + x * 18 * u - 16 * u, cy + 20 * u, cx + x * 18 * u + 16 * u, cy + 52 * u], outline="#ff5a5f", width=int(7 * u))
    return im


def nails(w, h):
    im = Image.new("RGB", (w, h), "#f2ece4")
    d = ImageDraw.Draw(im)
    u = w / 600
    cx, cy = w * .5, h * .55
    d.ellipse([cx - 120 * u, cy - 40 * u, cx + 120 * u, cy + 130 * u], fill="#c98d5a")  # pad area
    d.ellipse([cx - 55 * u, cy + 10 * u, cx + 55 * u, cy + 95 * u], fill="#3b2a24")  # main pad
    for i, x in enumerate((-90, -32, 32, 90)):
        tx, ty = cx + x * u, cy - 55 * u + (abs(x) > 60) * 25 * u
        d.ellipse([tx - 30 * u, ty - 32 * u, tx + 30 * u, ty + 32 * u], fill="#c98d5a")
        d.ellipse([tx - 18 * u, ty - 12 * u, tx + 18 * u, ty + 22 * u], fill="#3b2a24")
        d.polygon([(tx - 8 * u, ty - 30 * u), (tx + 8 * u, ty - 30 * u), (tx, ty - 50 * u)], fill="#7d7d7d")  # neat nail
    sparkle(d, w * .82, h * .22, 22 * u, "#ffcf4a")
    return im


def prices_png():
    im = Image.new("RGB", (900, 680), "#fff7ec")
    d = ImageDraw.Draw(im)
    t, f, b = ImageFont.truetype(BOLD, 46), ImageFont.truetype(FONT, 30), ImageFont.truetype(BOLD, 30)
    d.text((450, 60), "PRICE LIST", font=t, fill="#b5542c", anchor="mm")
    rows = [("", "Wash", "Groom"), ("Small", "$55", "$85"), ("Medium", "$70", "$105"), ("Large", "$90", "$135"),
            ("Nails", "$20", ""), ("Puppy", "$45", ""), ("De-shed", "+$25", "")]
    for i, r in enumerate(rows):
        y = 140 + i * 66
        for x, txt in zip((90, 470, 700), r):
            d.text((x, y), txt, font=b if i == 0 or x == 90 else f, fill="#3a2a20")
        if i:
            d.line([(80, y - 14), (820, y - 14)], fill="#e5d3bb", width=2)
    d.text((450, 640), "Ask us about matted coats!", font=f, fill="#7a6a5a", anchor="mm")
    return im


def noisy(im, amount):
    """Add camera-like grain so a JPEG comes out photo-sized."""
    rnd = random.Random(4032)
    px = im.load()
    for y in range(im.height):
        for x in range(im.width):
            n = rnd.randint(-amount, amount)
            r, g, b = px[x, y]
            px[x, y] = (max(0, min(255, r + n)), max(0, min(255, g + n)), max(0, min(255, b + n)))
    return im


def jpeg_near(im, path, target, q0=95):
    """Save a JPEG as close to target bytes as the quality steps allow."""
    best = None
    for q in range(q0, 20, -2):
        im.save(path, "JPEG", quality=q)
        size = path.stat().st_size
        if best is None or abs(size - target) < abs(best[1] - target):
            best = (q, size)
    im.save(path, "JPEG", quality=best[0])
    return path.stat().st_size


def webp_near(im, path, target):
    best = None
    for q in range(95, 5, -5):
        im.save(path, "WEBP", quality=q, method=6)
        size = path.stat().st_size
        if best is None or abs(size - target) < abs(best[1] - target):
            best = (q, size)
    im.save(path, "WEBP", quality=best[0], method=6)
    return path.stat().st_size


def main():
    b, a = SITE / "broken" / "images", SITE / "fixed" / "images"
    b.mkdir(parents=True, exist_ok=True)
    a.mkdir(parents=True, exist_ok=True)
    sizes = {}
    # before: the hero as it came off the camera: 2400 px wide, 1.2 MB
    big = noisy(hero(2400, 1500).filter(ImageFilter.GaussianBlur(1)), 14)
    sizes["IMG_4032.jpg"] = jpeg_near(big, b / "IMG_4032.jpg", 1214541, q0=100)
    for name, fn, target in (("photo1.jpg", wash, 120835), ("photo2.jpg", clip, 101500), ("photo3.jpg", nails, 81574)):
        im = noisy(fn(1200, 800).filter(ImageFilter.GaussianBlur(1)), 6)
        sizes[name] = jpeg_near(im, b / name, target)
    prices_png().save(b / "prices.png", optimize=True)
    sizes["prices.png"] = (b / "prices.png").stat().st_size
    # after: the right size, WebP
    sizes["dog-grooming-geelong-hero.webp"] = webp_near(hero(1200, 750), a / "dog-grooming-geelong-hero.webp", 13270)
    for name, fn, target in (("dog-wash-blow-dry.webp", wash, 4130), ("dog-full-groom-clip.webp", clip, 4982), ("dog-nail-trim.webp", nails, 3736)):
        sizes[name] = webp_near(fn(600, 400), a / name, target)
    for k, v in sizes.items():
        print(f"{k:34} {v:>9,}")


if __name__ == "__main__":
    main()
