"""prep_shot.py src dst width [--notrim]
Trims empty background below the content (keeps a margin), then scales to width."""
import sys
from PIL import Image, ImageChops
src, dst, width = sys.argv[1], sys.argv[2], int(sys.argv[3])
im = Image.open(src).convert("RGB")
if "--notrim" not in sys.argv:
    bg = Image.new("RGB", im.size, im.getpixel((im.width - 2, im.height - 2)))
    box = ImageChops.difference(im, bg).convert("L").point(lambda v: 255 if v > 12 else 0).getbbox()
    if box:
        bottom = min(im.height, box[3] + int(im.width * 0.03))
        im = im.crop((0, 0, im.width, bottom))
h = round(im.height * width / im.width)
im.resize((width, h), Image.LANCZOS).save(dst, optimize=True)
print(dst, width, h)
