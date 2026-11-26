"""Builds the Bayside Paws brand kit into ../build/brand-kit:
logo (SVG + PNG), colour palette, brand and voice guide (PDF) and six sample posts.
Needs Pillow, Node + Playwright, and the Inter font. Run: python make_brand_kit.py"""
import importlib.util
import os
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "build", "brand-kit")
WORK = os.path.join(HERE, "..", "build", "_kit_work")
os.makedirs(os.path.join(OUT, "sample-posts"), exist_ok=True)
os.makedirs(WORK, exist_ok=True)

# the same dog drawings as the SEO Basics practice site
spec = importlib.util.spec_from_file_location("art", os.path.join(HERE, "..", "..", "seo", "src", "make_images.py"))
art = importlib.util.module_from_spec(spec)
spec.loader.exec_module(art)

COLOURS = [("Harbour Rust", "#B5542C", "Logo, headings, buttons"), ("Golden Fur", "#E0A43A", "Highlights, offer badges"),
           ("Warm Cream", "#FFFAF3", "Backgrounds"), ("Charcoal", "#2B2622", "Text"), ("Calm Sage", "#5E9C8F", "Tips and calm topics")]

LOGO_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 160" width="600" height="160">
  <circle cx="80" cy="80" r="72" fill="#B5542C"/>
  <g fill="#FFFAF3">
    <ellipse cx="80" cy="98" rx="27" ry="22"/>
    <ellipse cx="50" cy="70" rx="11" ry="14" transform="rotate(-18 50 70)"/>
    <ellipse cx="68" cy="52" rx="11" ry="14" transform="rotate(-6 68 52)"/>
    <ellipse cx="92" cy="52" rx="11" ry="14" transform="rotate(6 92 52)"/>
    <ellipse cx="110" cy="70" rx="11" ry="14" transform="rotate(18 110 70)"/>
  </g>
  <text x="172" y="84" font-family="Inter, Arial, sans-serif" font-weight="800" font-size="50" fill="#2B2622">Bayside Paws</text>
  <text x="174" y="118" font-family="Inter, Arial, sans-serif" font-weight="600" font-size="19" letter-spacing="3.2" fill="#B5542C">DOG GROOMING · GEELONG WEST</text>
</svg>"""
MARK_SVG = LOGO_SVG.split("<text")[0].replace('viewBox="0 0 600 160" width="600" height="160"', 'viewBox="0 0 160 160" width="160" height="160"') + "</svg>"

BASE_CSS = """
@font-face{font-family:Inter;src:local('Inter')}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:Inter,sans-serif;color:#2B2622;background:#FFFAF3}
.post{position:relative;width:1080px;height:1350px;overflow:hidden;background:#FFFAF3}
.story{height:1920px}
.mark{position:absolute;right:56px;bottom:56px;width:120px;height:120px}
.tag{display:inline-block;font-weight:800;font-size:30px;letter-spacing:4px;text-transform:uppercase;padding:14px 26px;border-radius:999px}
h1{font-weight:800;letter-spacing:-2px;line-height:1.02}
p{line-height:1.35}
"""


def write(name, html):
    path = os.path.join(WORK, name)
    open(path, "w").write(html)
    return path


def art_png(fn, w, h, name):
    p = os.path.join(WORK, name)
    fn(w, h).save(p)
    return name


def page(body, extra=""):
    return f"<!doctype html><html><head><meta charset='utf-8'><style>{BASE_CSS}{extra}</style></head><body>{body}</body></html>"


def posts():
    mark = f"<div class='mark'>{MARK_SVG.replace('<svg ', '<svg style=\"width:120px;height:120px\" ')}</div>"
    hero = art_png(art.hero, 1080, 760, "hero.png")
    wash = art_png(art.wash, 1080, 720, "wash.png")
    clip = art_png(art.clip, 1080, 720, "clip.png")
    nails = art_png(art.nails, 1080, 700, "nails.png")
    out = {}
    out["1-grooming-tip-carousel-cover"] = page(f"""<div class='post' style='background:#5E9C8F;color:#FFFAF3;padding:110px 90px'>
      <span class='tag' style='background:#FFFAF3;color:#5E9C8F'>Grooming tips</span>
      <h1 style='font-size:118px;margin-top:70px'>How often should you groom your dog?</h1>
      <p style='font-size:52px;margin-top:60px;font-weight:600'>Every 4 to 12 weeks, depending on the coat.</p>
      <p style='font-size:40px;margin-top:150px;font-weight:700;color:#FFE3A8'>Swipe for your dog's coat type →</p>{mark}</div>""")
    out["2-happy-dogs-meet-biscuit"] = page(f"""<div class='post'>
      <img src='{hero}' style='width:1080px;height:760px;display:block'>
      <div style='padding:60px 90px'><span class='tag' style='background:#E0A43A;color:#2B2622'>Happy dogs</span>
      <h1 style='font-size:110px;margin-top:40px;color:#B5542C'>Meet Biscuit</h1>
      <p style='font-size:46px;margin-top:22px'>Fresh teddy-bear trim, same waggy tail.</p></div>{mark}</div>""")
    out["3-behind-the-scenes-calm-grooms"] = page(f"""<div class='post' style='padding:110px 90px'>
      <span class='tag' style='background:#2B2622;color:#FFFAF3'>Behind the scenes</span>
      <h1 style='font-size:96px;margin-top:60px'>How we keep anxious dogs calm</h1>
      <ul style='font-size:48px;margin-top:60px;list-style:none;line-height:1.5'>
        <li>🐾 One dog at a time</li><li>🐾 Quiet dryers</li><li>🐾 Breaks whenever they need one</li><li>🐾 Never left in a cage</li></ul>
      <img src='{clip}' style='position:absolute;left:0;bottom:-40px;width:760px;opacity:.95'>{mark}</div>""")
    out["4-offer-puppy-intro-groom"] = page(f"""<div class='post'>
      <img src='{wash}' style='width:1080px;height:720px;display:block'>
      <div style='position:absolute;top:60px;right:60px;width:250px;height:250px;border-radius:50%;background:#E0A43A;display:flex;
        flex-direction:column;align-items:center;justify-content:center;transform:rotate(8deg)'>
        <span style='font-size:100px;font-weight:800;line-height:1'>$45</span><span style='font-size:28px;font-weight:700'>under 6 months</span></div>
      <div style='padding:60px 90px'><span class='tag' style='background:#B5542C;color:#FFFAF3'>Offers & news</span>
      <h1 style='font-size:104px;margin-top:40px;color:#B5542C'>Puppy intro grooms</h1>
      <p style='font-size:44px;margin-top:22px'>Short, gentle and cage-free, so grooming feels fun from day one.</p></div>{mark}</div>""")
    out["5-story-walk-in-nail-trims"] = page(f"""<div class='post story' style='background:#B5542C;color:#FFFAF3;padding:200px 90px'>
      <span class='tag' style='background:#FFFAF3;color:#B5542C'>This Saturday</span>
      <h1 style='font-size:140px;margin-top:70px'>Walk-in nail trims</h1>
      <p style='font-size:72px;margin-top:40px;font-weight:800;color:#FFE3A8'>8am to 12pm · $20</p>
      <p style='font-size:46px;margin-top:30px'>No booking needed. 14 Pakington Street.</p>
      <img src='{nails}' style='position:absolute;left:0;top:960px;width:1080px;height:700px'>{mark.replace("bottom:56px", "bottom:300px")}</div>""")
    out["6-news-holiday-hours"] = page(f"""<div class='post' style='padding:110px 90px'>
      <span class='tag' style='background:#B5542C;color:#FFFAF3'>Offers & news</span>
      <h1 style='font-size:110px;margin-top:60px'>Holiday hours</h1>
      <table style='font-size:50px;margin-top:70px;border-collapse:collapse;width:100%'>
        <tr><td style='padding:22px 0;border-bottom:3px solid #EAD9C2'>Wed 24 Dec</td><td style='text-align:right;font-weight:800;border-bottom:3px solid #EAD9C2'>8am – 2pm</td></tr>
        <tr><td style='padding:22px 0;border-bottom:3px solid #EAD9C2'>25 – 28 Dec</td><td style='text-align:right;font-weight:800;border-bottom:3px solid #EAD9C2'>Closed</td></tr>
        <tr><td style='padding:22px 0;border-bottom:3px solid #EAD9C2'>From Tue 30 Dec</td><td style='text-align:right;font-weight:800;border-bottom:3px solid #EAD9C2'>Usual hours</td></tr></table>
      <p style='font-size:44px;margin-top:80px;color:#B5542C;font-weight:700'>Book your Christmas groom early 🎄</p>{mark}</div>""")
    return out


def palette_html():
    sw = "".join(f"<div style='flex:1;display:flex;flex-direction:column'><div style='height:300px;background:{h};border:2px solid #EAD9C2'></div>"
                 f"<p style='font-size:30px;font-weight:800;margin-top:20px'>{n}</p><p style='font-size:28px'>{h}</p>"
                 f"<p style='font-size:24px;color:#6b5f55'>{u}</p></div>" for n, h, u in COLOURS)
    return page(f"<div style='width:1600px;height:560px;padding:60px 70px'><h1 style='font-size:60px'>Bayside Paws colours</h1>"
                f"<div style='display:flex;gap:30px;margin-top:50px'>{sw}</div>"
                f"<p style='font-size:26px;margin-top:40px'>Font: Inter (ExtraBold for headings, Regular for text). Free on Google Fonts and in Canva.</p></div>")


def guide_html():
    sw = "".join(f"<td><div style='height:40px;background:{h};border:1px solid #EAD9C2;border-radius:8px'></div><b>{n}</b><br>{h}<br><small>{u}</small></td>"
                 for n, h, u in COLOURS)
    css = """@page{size:A4;margin:13mm 15mm}
    body{font-size:9.8pt;background:#fff}
    h1{font-size:28pt;letter-spacing:-.5px;margin:0 0 4pt}
    h2{color:#B5542C;font-size:14pt;margin:12pt 0 4pt}
    p,li{line-height:1.38;margin:2pt 0}
    ul{padding-left:16pt}
    table{border-collapse:collapse;width:100%;margin:6pt 0}
    td,th{border:1px solid #EAD9C2;padding:3pt 6pt;vertical-align:top;text-align:left}
    th{background:#2B2622;color:#fff}
    .sw td{border:0;width:20%;font-size:9pt}
    .box{background:#FFF6E8;border-left:5px solid #E0A43A;padding:8pt 10pt;margin:6pt 0;white-space:pre-line}
    .pb{break-before:page}"""
    body = f"""
    <div style='margin-bottom:10pt'>{LOGO_SVG.replace('width="600" height="160"', 'width="330" height="88"')}</div>
    <h1>Brand and voice guide</h1>
    <p style='color:#6b5f55'>Bayside Paws Dog Grooming · 14 Pakington Street, Geelong West VIC 3218 · (03) 5550 0142 · @baysidepawsgeelong<br>
    A made-up business for Avro Academy's Social Media Marketing for Small Business course.</p>
    <h2>Who we are</h2>
    <p>A small, cage-free dog grooming salon in Geelong West, run by Mia, a former vet nurse, since 2019. We groom one dog at a time, by hand,
    at the dog's pace. Our customers are busy local dog owners and new puppy owners who want a gentle, trustworthy groomer.</p>
    <h2>Our voice</h2>
    <table><tr><th>We are</th><th>We are not</th></tr>
    <tr><td>Warm and friendly</td><td>Gushing or over the top</td></tr>
    <tr><td>Knowledgeable and plain-spoken</td><td>Full of jargon</td></tr>
    <tr><td>Calm and reassuring</td><td>Pushy ("BOOK NOW!!!")</td></tr>
    <tr><td>A little playful</td><td>Silly about animal welfare</td></tr></table>
    <table><tr><th>Say</th><th>Rather than</th></tr>
    <tr><td>"Biscuit was a star on the table today."</td><td>"OMG cutest pupper EVER!!! 😍😍😍"</td></tr>
    <tr><td>"Curly coats knot easily, so we suggest a groom every 4–6 weeks."</td><td>"Regular maintenance is required to prevent matting of the coat."</td></tr>
    <tr><td>"We've got two spots left on Saturday if you need one."</td><td>"HURRY! LAST CHANCE! Book now before it's too late!"</td></tr></table>
    <ul><li>Write like Mia talks at the counter: short sentences, everyday words.</li>
    <li>Use the dog's name (with the owner's permission). Never share owners' details.</li>
    <li>Emoji are seasoning: 1–3 per post, never instead of words. 🐾 ✂️ 🛁 are ours.</li>
    <li>Hashtags: 3–5, in CamelCase: #DogGroomingGeelong #GeelongDogs #CageFreeGrooming #BaysidePawsPup</li>
    <li>One call to action per post: book via the link in bio, call (03) 5550 0142, save this, or tag a friend.</li>
    <li>Check prices, dates and spelling every time. No "best in Geelong" claims, no fake urgency.</li></ul>
    <h2 class='pb'>Logo</h2>
    <p>Use the full logo on the website and printed material, and the paw mark on its own for profile pictures and posts.
    On posts, the paw mark goes in the <b>bottom-right corner</b>, small, with space around it. Don't stretch, recolour or add effects to it.</p>
    <p>Files: <code>logo/bayside-paws-logo.svg</code> and <code>.png</code>, <code>logo/bayside-paws-paw-mark.svg</code> and <code>.png</code>.</p>
    <h2>Colours</h2>
    <table class='sw'><tr>{sw}</tr></table>
    <p>Rust and charcoal on cream are the everyday look. Golden Fur is for highlights and offers; Calm Sage is for tips. Keep strong contrast for text.</p>
    <h2>Fonts</h2>
    <p><b style='font-weight:800'>Inter ExtraBold</b> for headings and big text on graphics. Inter Regular for everything else.
    Inter is free (Google Fonts) and built into Canva.</p>
    <h2>Photos and video</h2>
    <ul><li>Window light or outside in the shade; no flash. Clean background (move the mop and the bins).</li>
    <li>Shoot at the dog's eye level. Before and afters: same angle, same light, same spot.</li>
    <li>Vertical: 4:5 for feed posts (1080 × 1350), 9:16 for stories and Reels (1080 × 1920).</li>
    <li>Always ask the owner first, and credit reposts ("📸 by @sarahandbiscuit").</li></ul>
    <h2>Graphics</h2>
    <ul><li>One message per graphic, big short text, brand colours and Inter every time.</li>
    <li>Leave a margin: grids and story buttons cut off the edges. Leave space at the bottom of stories for a link sticker.</li></ul>
    <h2>Profile</h2>
    <div class='box'>🐾 Cage-free dog grooming in Geelong West
    Gentle grooms for anxious pups and seniors
    ✂️ Tue–Sat · 14 Pakington St
    👇 Book your groom</div>
    <h2>The six sample posts</h2>
    <table><tr><th>File</th><th>Pillar and format</th><th>One message</th></tr>
    <tr><td>1-grooming-tip-carousel-cover.png</td><td>Grooming tips · carousel cover</td><td>How often to groom</td></tr>
    <tr><td>2-happy-dogs-meet-biscuit.png</td><td>Happy dogs · photo</td><td>Biscuit's teddy-bear trim</td></tr>
    <tr><td>3-behind-the-scenes-calm-grooms.png</td><td>Behind the scenes · photo</td><td>How we keep anxious dogs calm</td></tr>
    <tr><td>4-offer-puppy-intro-groom.png</td><td>Offers &amp; news · photo</td><td>Puppy intro grooms, $45</td></tr>
    <tr><td>5-story-walk-in-nail-trims.png</td><td>Offers &amp; news · story (1080 × 1920)</td><td>Walk-in nail trims this Saturday</td></tr>
    <tr><td>6-news-holiday-hours.png</td><td>Offers &amp; news · photo</td><td>Christmas opening hours</td></tr></table>
    <p style='color:#6b5f55;font-size:9pt'>The pictures are illustrations. On the real account, use your own photos of real dogs, with permission.</p>
"""
    return f"<!doctype html><html><head><meta charset='utf-8'><style>{BASE_CSS}{css}</style></head><body>{body}</body></html>"


SHOT_JS = """const { chromium } = require('playwright');
(async () => { const b = await chromium.launch(); const jobs = JSON.parse(process.argv[2]);
  for (const j of jobs) { const p = await b.newPage({ viewport: { width: j.w, height: j.h } });
    await p.goto('file://' + j.html); await p.waitForTimeout(300);
    if (j.pdf) await p.pdf({ path: j.out, format: 'A4', printBackground: true, preferCSSPageSize: true });
    else await p.screenshot({ path: j.out, omitBackground: !!j.transparent }); await p.close(); }
  await b.close(); })();"""


def main():
    import json
    os.makedirs(os.path.join(OUT, "logo"), exist_ok=True)
    open(os.path.join(OUT, "logo", "bayside-paws-logo.svg"), "w").write(LOGO_SVG)
    open(os.path.join(OUT, "logo", "bayside-paws-paw-mark.svg"), "w").write(MARK_SVG)
    jobs = []
    for name, html in posts().items():
        jobs.append({"html": write(name + ".html", html), "out": os.path.join(OUT, "sample-posts", name + ".png"),
                     "w": 1080, "h": 1920 if "story" in name else 1350})
    logo_page = "<!doctype html><html><head><style>body{margin:0;background:transparent}svg{display:block}</style></head><body>%s</body></html>"
    jobs.append({"html": write("logo.html", logo_page % LOGO_SVG.replace('width="600" height="160"', 'width="1800" height="480"')),
                 "out": os.path.join(OUT, "logo", "bayside-paws-logo.png"), "w": 1800, "h": 480, "transparent": True})
    jobs.append({"html": write("mark.html", logo_page % MARK_SVG.replace('width="160" height="160"', 'width="800" height="800"')),
                 "out": os.path.join(OUT, "logo", "bayside-paws-paw-mark.png"), "w": 800, "h": 800, "transparent": True})
    jobs.append({"html": write("palette.html", palette_html()), "out": os.path.join(OUT, "colour-palette.png"), "w": 1600, "h": 560})
    jobs.append({"html": write("guide.html", guide_html()), "out": os.path.join(OUT, "Brand-and-Voice-Guide.pdf"), "w": 1000, "h": 1400, "pdf": True})
    js = os.path.join(WORK, "shot.js")
    open(js, "w").write(SHOT_JS)
    subprocess.run(["node", js, json.dumps(jobs)], check=True)
    # shrink the PNG posts a little
    from PIL import Image
    for f in os.listdir(os.path.join(OUT, "sample-posts")):
        p = os.path.join(OUT, "sample-posts", f)
        Image.open(p).convert("RGB").quantize(colors=128, method=Image.Quantize.MEDIANCUT).save(p, optimize=True)
    open(os.path.join(OUT, "README.txt"), "w").write(
        "Bayside Paws brand kit (Social Media Marketing for Small Business, Avro Academy)\n\n"
        "Brand-and-Voice-Guide.pdf  voice, logo, colours, fonts, photo style, profile and the sample posts\n"
        "logo/                      full logo and paw mark, SVG and PNG (transparent)\n"
        "colour-palette.png         the five brand colours with hex codes\n"
        "sample-posts/              six sample posts (1080 x 1350; the story is 1080 x 1920)\n\n"
        "Bayside Paws is a made-up business. Use and adapt these files for your course work.\n")
    print("built", OUT)


if __name__ == "__main__":
    main()
