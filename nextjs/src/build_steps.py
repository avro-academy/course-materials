"""Builds step-1-start ... step-7-final from final/ plus overrides/. Usage: python build_steps.py <out folder>"""
import os, re, shutil, sys
HERE = os.path.dirname(os.path.abspath(__file__))
FINAL = os.path.join(HERE, "final")
OUT = sys.argv[1]
STEPS = ["step-1-start", "step-2-components", "step-3-routing", "step-4-styling", "step-5-server-client", "step-6-forms", "step-7-final"]
COMMON = [".gitignore", "AGENTS.md", "eslint.config.mjs", "package.json", "package-lock.json", "tsconfig.json", "next.config.ts"]

def rd(rel): return open(os.path.join(FINAL, rel), encoding="utf-8").read()
def wr(step, rel, text):
    p = os.path.join(OUT, step, rel); os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8").write(text)
def cp(step, rel, src=FINAL):
    p = os.path.join(OUT, step, rel); os.makedirs(os.path.dirname(p), exist_ok=True)
    (shutil.copytree if os.path.isdir(os.path.join(src, rel)) else shutil.copy)(os.path.join(src, rel), p)
def overrides(step, key):
    base = os.path.join(HERE, "overrides", key)
    for root, _, files in os.walk(base):
        for f in files:
            rel = os.path.relpath(os.path.join(root, f), base); cp(step, rel, base)
def sub(text, old, new):
    assert old in text, old[:60]; return text.replace(old, new)

CONFIG_DEFAULT = re.sub(r"        // Avro Academy change.*?\n.*?\n        condition: .*?\n", "", rd("next.config.ts"), flags=re.S)
for i, step in enumerate(STEPS, 1):
    for f in COMMON: cp(step, f)
    if i < 4: wr(step, "next.config.ts", CONFIG_DEFAULT)
    if i < 7: shutil.copy(os.path.join(HERE, "favicon.ico"), os.path.join(OUT, step, "app", "favicon.ico")) if os.path.isdir(os.path.join(OUT, step, "app")) else None

# 1-3: hand-written
for i, key in [(1, "s1"), (2, "s2"), (3, "s3")]:
    overrides(STEPS[i - 1], key)
    os.makedirs(os.path.join(OUT, STEPS[i - 1], "public"), exist_ok=True)
    shutil.copy(os.path.join(HERE, "favicon.ico"), os.path.join(OUT, STEPS[i - 1], "app", "favicon.ico"))
for i in (2, 3): cp(STEPS[i - 1], "lib/menu.ts")

# 4-6: final minus later features
LAYOUT_4 = sub(sub(rd("app/layout.tsx"), '''  metadataBase: new URL(process.env.SITE_URL ?? "http://localhost:3000"),
  title: {
    template: "%s | Corner Café",
    default: "Corner Café — coffee, food and good company",
  },
  description: "A friendly neighbourhood café in Sydney. See the menu, today's special and book a table.",''', '''  title: "Corner Café",
  description: "A friendly neighbourhood café in Sydney.",'''), "x", "x")
HEADER_PLAIN = sub(sub(rd("components/SiteHeader.tsx"), 'import NavLink from "./NavLink";\n', ""),
    '''          <NavLink href="/">Home</NavLink>
          <NavLink href="/menu">Menu</NavLink>
          <NavLink href="/book">Book a table</NavLink>
          <NavLink href="/about">About</NavLink>''',
    '''          <Link href="/" className="rounded-full px-3 py-1.5 text-stone-100 hover:bg-white/10">Home</Link>
          <Link href="/menu" className="rounded-full px-3 py-1.5 text-stone-100 hover:bg-white/10">Menu</Link>
          <Link href="/about" className="rounded-full px-3 py-1.5 text-stone-100 hover:bg-white/10">About</Link>''')
HEADER_5 = sub(rd("components/SiteHeader.tsx"), '          <NavLink href="/book">Book a table</NavLink>\n', "")
BOOK_BTN = '''          <Link href="/book" className="rounded-full bg-white px-5 py-2.5 font-semibold ring-1 ring-stone-300 hover:bg-stone-100">
            Book a table
          </Link>
'''
HOME_5 = sub(rd("app/page.tsx"), BOOK_BTN, "")
HOME_4 = sub(sub(sub(sub(HOME_5, '''        <Suspense fallback={<p className="text-sm text-stone-400">Checking opening hours…</p>}>
          <OpenNow />
        </Suspense>
        <h1 className="mt-3''', '''        <h1 className="'''), '''      <Suspense fallback={<div className="h-48 rounded-2xl bg-amber-50" />}>
        <TodaysSpecial />
      </Suspense>

      <h2 className="mt-12''', '''      <h2 className="mt-4'''), 'import { Suspense } from "react";\n', ""),
    'import OpenNow from "@/components/OpenNow";\nimport TodaysSpecial from "@/components/TodaysSpecial";\n', "")
MENU_6 = re.sub(r'import type \{ Metadata \} from "next";\n|export const metadata: Metadata = \{.*?\};\n\n', "", rd("app/menu/page.tsx"), flags=re.S)
MENU_4 = '''import MenuCard from "@/components/MenuCard";
import { MENU } from "@/lib/menu";

export default function MenuPage() {
  return (
    <>
      <h1 className="text-3xl font-extrabold">Our menu</h1>
      <p className="mt-2 text-stone-600">Everything is made fresh in our kitchen. Prices include GST.</p>
      <div className="mt-6 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
        {MENU.map((item, index) => (
          <MenuCard key={item.slug} item={item} eager={index < 3} />
        ))}
      </div>
    </>
  );
}
'''
ITEM_6 = re.sub(r'export async function generateMetadata.*?\n}\n\n', "", sub(rd("app/menu/[slug]/page.tsx"), 'import type { Metadata } from "next";\n', ""), flags=re.S)
ABOUT_6 = sub(sub(re.sub(r'export const metadata: Metadata = \{.*?\};\n\n', "", sub(rd("app/about/page.tsx"), 'import type { Metadata } from "next";\n', ""), flags=re.S),
    '// Read on the server. Set CAFE_PHONE in .env.local (or in your hosting settings).\nconst phone = process.env.CAFE_PHONE ?? "(02) 5550 0000";\n\n', ""), "{phone}", "(02) 5550 0000")
ABOUT_4 = '''export default function AboutPage() {
  return (
    <div className="max-w-2xl py-4">
      <h1 className="text-3xl font-extrabold">About Corner Café</h1>
      <p className="mt-4 text-stone-700">
        We&apos;re a small neighbourhood café run by a team of locals. We roast our beans in Marrickville, bake every
        morning and know most of our regulars by name.
      </p>
      <p className="mt-4 text-stone-700">
        Find us at <strong>12 King Street, Newtown NSW</strong>.
      </p>
    </div>
  );
}
'''
BOOK_6 = re.sub(r'export const metadata: Metadata = \{.*?\};\n\n', "", sub(rd("app/book/page.tsx"), 'import type { Metadata } from "next";\n', ""), flags=re.S)

for i in (4, 5, 6):
    s = STEPS[i - 1]
    for rel in ["app/globals.css", "app/not-found.tsx", "components/MenuCard.tsx", "components/VegBadge.tsx", "components/VegBadge.module.css",
                "components/SiteFooter.tsx", "lib/menu.ts", "public"]:
        cp(s, rel)
    shutil.copy(os.path.join(HERE, "favicon.ico"), os.path.join(OUT, s, "app", "favicon.ico"))
    wr(s, "app/layout.tsx", LAYOUT_4)
    wr(s, "app/menu/[slug]/page.tsx", ITEM_6)
    if i == 4:
        wr(s, "components/SiteHeader.tsx", HEADER_PLAIN); wr(s, "app/page.tsx", HOME_4); wr(s, "app/menu/page.tsx", MENU_4); wr(s, "app/about/page.tsx", ABOUT_4)
    else:
        for rel in ["components/NavLink.tsx", "components/MenuFilter.tsx", "components/OpenNow.tsx", "components/TodaysSpecial.tsx",
                    "lib/hours.ts", "lib/specials.ts", "app/error.tsx"]:
            cp(s, rel)
        wr(s, "app/menu/page.tsx", MENU_6); wr(s, "app/about/page.tsx", ABOUT_6)
        wr(s, "components/SiteHeader.tsx", HEADER_5 if i == 5 else rd("components/SiteHeader.tsx"))
        wr(s, "app/page.tsx", HOME_5 if i == 5 else rd("app/page.tsx"))
    if i == 6:
        for rel in ["app/book/actions.ts", "app/book/BookingForm.tsx", "app/api", "lib/booking.ts"]: cp(s, rel)
        wr(s, "app/book/page.tsx", BOOK_6)
# 7: the finished app
for rel in ["app", "components", "lib", "public", ".env.example"]: cp(STEPS[6], rel)
print("built", len(STEPS), "steps")
