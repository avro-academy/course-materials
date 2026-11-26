"""Builds the Social Media Marketing files into ../build:
Bayside-Paws-Insights-Practice.xlsx (from ../data/Bayside-Paws-Insights-Export.csv),
Social-Media-Content-Calendar.xlsx, Monthly-Social-Media-Report-Template.docx,
Social-Media-Plan-Template.docx."""
import csv
import os

from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor
from openpyxl import Workbook
from openpyxl.formatting.rule import CellIsRule, ColorScaleRule
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.worksheet.datavalidation import DataValidation

HERE = os.path.dirname(os.path.abspath(__file__))
BUILD = os.path.join(HERE, "..", "build")
DATA = os.path.join(HERE, "..", "data", "Bayside-Paws-Insights-Export.csv")
os.makedirs(BUILD, exist_ok=True)

NAVY = PatternFill("solid", fgColor="1D2B4F")
YEL = PatternFill("solid", fgColor="FFF6D6")
GREEN = PatternFill("solid", fgColor="D5F0E3")
WHITE = Font(color="FFFFFF", bold=True)
BOLD = Font(bold=True)
TITLE = Font(bold=True, size=14, color="1D2B4F")
NOTE = Font(italic=True, color="56607A")
WRAP = Alignment(wrap_text=True, vertical="top")
PILLARS = ["Grooming tips", "Happy dogs", "Behind the scenes", "Offers & news"]
FORMATS = ["Reel", "Carousel", "Photo", "Story"]


def head(ws, cols, widths, row=1):
    for i, (c, w) in enumerate(zip(cols, widths), 1):
        cell = ws.cell(row=row, column=i, value=c)
        cell.fill, cell.font, cell.alignment = NAVY, WHITE, Alignment(wrap_text=True, vertical="center")
        if w:
            ws.column_dimensions[cell.column_letter].width = w
    ws.freeze_panes = ws.cell(row=row + 1, column=1)


def pick(ws, rng, options, prompt):
    dv = DataValidation(type="list", formula1='"' + ",".join(options) + '"', allow_blank=True)
    dv.promptTitle, dv.prompt = "Choose one", prompt
    ws.add_data_validation(dv)
    dv.add(rng)


# ---------------------------------------------------------------- practice workbook
def practice_workbook():
    rows = list(csv.DictReader(open(DATA)))
    n = len(rows)
    last = n + 1
    wb = Workbook()
    ws = wb.active
    ws.title = "Read me"
    for i, t in enumerate([
        "Bayside Paws: three months of Instagram and Facebook results (made-up, but realistic)",
        "72 posts, 1 July to 30 September 2026. Social Media Marketing for Small Business, Module 6.",
        "",
        "Posts: one row per post. Engagement rate = (likes + comments + shares + saves) ÷ reach, worked out in column N.",
        "Bookings = new customers who said that post was how they heard about Bayside Paws (Mia asks every new customer).",
        "Summary: averages by content pillar, by format, by time of day and by platform, worked out from the Posts sheet with formulas.",
        "",
        "Try it:",
        "1. Sort the Posts sheet by engagement rate (Data > Sort, largest to smallest). Which 3 posts did best? What do they have in common?",
        "2. Does posting time matter? Compare posts at 18:00–20:00 with morning and lunchtime posts (Summary, time of day).",
        "3. Instagram vs Facebook: which gets more reach for Bayside Paws?",
        "4. Write three changes you'd make to Mia's plan next month, based on the data.",
        "",
        "The raw export (Bayside-Paws-Insights-Export.csv) has the same posts without the extra columns, to analyse yourself.",
    ], 1):
        c = ws.cell(row=i, column=1, value=t)
        c.font = TITLE if i == 1 else (BOLD if t == "Try it:" else Font())
    ws.column_dimensions["A"].width = 120

    s = wb.create_sheet("Posts")
    cols = ["Date", "Time", "Platform", "Format", "Pillar", "Post", "Reach", "Likes", "Comments", "Shares", "Saves", "Link clicks",
            "Bookings", "Engagement rate", "Time of day", "Month"]
    head(s, cols, [11, 7, 11, 10, 17, 40, 8, 7, 9, 7, 7, 9, 9, 11, 13, 8])
    for r, row in enumerate(rows, 2):
        y, m, d = (int(x) for x in row["date"].split("-"))
        from datetime import date
        s.cell(row=r, column=1, value=date(y, m, d)).number_format = "ddd d mmm"
        vals = [row["time"], row["platform"], row["format"], row["pillar"], row["post"]] + [int(row[k]) for k in
                ("reach", "likes", "comments", "shares", "saves", "link_clicks", "bookings")]
        for c, v in enumerate(vals, 2):
            s.cell(row=r, column=c, value=v)
        s.cell(row=r, column=14, value=f"=(H{r}+I{r}+J{r}+K{r})/G{r}").number_format = "0.0%"
        s.cell(row=r, column=15, value=f'=IF(VALUE(LEFT(B{r},2))>=18,"Evening",IF(VALUE(LEFT(B{r},2))>=11,"Lunchtime","Morning"))')
        s.cell(row=r, column=16, value=f'=TEXT(A{r},"mmm")')
    s.auto_filter.ref = f"A1:P{last}"
    s.conditional_formatting.add(f"N2:N{last}", ColorScaleRule(start_type="min", start_color="FFFFFF", end_type="max", end_color="63BE7B"))

    t = wb.create_sheet("Summary")
    t.column_dimensions["A"].width = 22
    for col in "BCDEFG":
        t.column_dimensions[col].width = 14

    def block(r0, title, key_col, keys, extra=True):
        t.cell(row=r0, column=1, value=title).font = TITLE
        hdr = ["", "Posts", "Avg reach", "Avg engagement rate"] + (["Avg saves", "Avg link clicks", "Bookings"] if extra else [])
        for i, h in enumerate(hdr, 1):
            c = t.cell(row=r0 + 1, column=i, value=h)
            c.fill, c.font = NAVY, WHITE
        rng = lambda col: f"Posts!${col}$2:${col}${last}"
        for k, key in enumerate(keys):
            r = r0 + 2 + k
            t.cell(row=r, column=1, value=key)
            t.cell(row=r, column=2, value=f"=COUNTIF({rng(key_col)},A{r})")
            t.cell(row=r, column=3, value=f"=AVERAGEIF({rng(key_col)},A{r},{rng('G')})").number_format = "#,##0"
            t.cell(row=r, column=4, value=f"=AVERAGEIF({rng(key_col)},A{r},{rng('N')})").number_format = "0.0%"
            if extra:
                t.cell(row=r, column=5, value=f"=AVERAGEIF({rng(key_col)},A{r},{rng('K')})").number_format = "0.0"
                t.cell(row=r, column=6, value=f"=AVERAGEIF({rng(key_col)},A{r},{rng('L')})").number_format = "0.0"
                t.cell(row=r, column=7, value=f"=SUMIF({rng(key_col)},A{r},{rng('M')})")
        r = r0 + 2 + len(keys)
        t.cell(row=r, column=1, value="All posts").font = BOLD
        t.cell(row=r, column=2, value=f"=COUNTA({rng('F')})").font = BOLD
        t.cell(row=r, column=3, value=f"=AVERAGE({rng('G')})").number_format = "#,##0"
        t.cell(row=r, column=4, value=f"=AVERAGE({rng('N')})").number_format = "0.0%"
        if extra:
            t.cell(row=r, column=5, value=f"=AVERAGE({rng('K')})").number_format = "0.0"
            t.cell(row=r, column=6, value=f"=AVERAGE({rng('L')})").number_format = "0.0"
            t.cell(row=r, column=7, value=f"=SUM({rng('M')})")
        return r + 2

    r = block(1, "Results by content pillar", "E", PILLARS)
    r = block(r, "Results by format", "D", FORMATS)
    r = block(r, "Results by time of day", "O", ["Morning", "Lunchtime", "Evening"])
    r = block(r, "Results by platform", "C", ["Instagram", "Facebook"])
    r = block(r, "Results by month", "P", ["Jul", "Aug", "Sep"])
    t.cell(row=r, column=1, value="Engagement rate here is the average of each post's rate, so every post counts equally.").font = NOTE
    wb.calculation.fullCalcOnLoad = True
    wb.save(os.path.join(BUILD, "Bayside-Paws-Insights-Practice.xlsx"))


# ---------------------------------------------------------------- content calendar
def calendar_workbook():
    wb = Workbook()
    ws = wb.active
    ws.title = "How to use"
    for i, t in enumerate([
        "Social media content calendar",
        "Each row is one post. Plan 2–4 weeks ahead, and leave gaps for timely posts. (Social Media Marketing, Module 2.)",
        "",
        "1. On the Calendar sheet, type your start date in C2. The dates fill themselves in for 30 days.",
        "2. For each post, choose the platform, format, pillar and status from the lists, and write the idea and call to action.",
        "3. Mix pillars and formats across the week. Bayside Paws aims for 30% tips, 30% happy dogs, 20% behind the scenes, 20% offers.",
        "4. Delete the rows for days you won't post, or add a second row for a day with two posts.",
        "5. Pillar mix (on the right of the Calendar sheet) counts your planned posts against the target share.",
        "",
        "A realistic starting point: Instagram 3 feed posts a week (one short video) plus stories on most working days; "
        "Facebook 2–3 posts a week; Google Business Profile 1 update a week.",
        "The Example sheet shows the first week of a Bayside Paws calendar.",
    ], 1):
        ws.cell(row=i, column=1, value=t).font = TITLE if i == 1 else Font()
    ws.column_dimensions["A"].width = 120

    cols = ["Date", "Platform", "Format", "Pillar", "Idea", "Caption hook (first line)", "Call to action", "Hashtags", "Alt text", "Status", "Link (with UTM)"]
    widths = [13, 13, 11, 17, 34, 34, 18, 26, 30, 11, 30]
    platforms = ["Instagram", "Facebook", "Instagram + Facebook", "TikTok", "LinkedIn", "Google Business Profile", "WhatsApp"]
    formats = ["Reel", "Carousel", "Photo", "Story", "Live", "Text update"]
    statuses = ["Idea", "Drafted", "Scheduled", "Posted"]

    s = wb.create_sheet("Calendar")
    s["A1"], s["B2"] = "30-day content calendar", "Start date:"
    s["A1"].font = TITLE
    s["C2"].fill = YEL
    s["D2"] = "← type the first day, e.g. 1/12/2026"
    s["D2"].font = NOTE
    head(s, cols, widths, row=4)
    for r in range(5, 35):
        s.cell(row=r, column=1, value=f'=IF($C$2="","",$C$2+{r - 5})').number_format = "ddd d mmm"
        for c in (5, 6, 8, 9, 11):
            s.cell(row=r, column=c).alignment = WRAP
    pick(s, "B5:B60", platforms, "Where will it go?")
    pick(s, "C5:C60", formats, "Which format?")
    pick(s, "D5:D60", PILLARS + ["Other"], "Which content pillar?")
    pick(s, "J5:J60", statuses, "Where is it up to?")
    s.conditional_formatting.add("J5:J60", CellIsRule(operator="equal", formula=['"Posted"'], fill=GREEN))
    s.conditional_formatting.add("J5:J60", CellIsRule(operator="equal", formula=['"Scheduled"'], fill=YEL))
    s["M4"], s["N4"], s["O4"], s["P4"] = "Pillar", "Posts", "Share", "Target"
    for c in ("M4", "N4", "O4", "P4"):
        s[c].fill, s[c].font = NAVY, WHITE
    for i, (p, target) in enumerate(zip(PILLARS, (0.3, 0.3, 0.2, 0.2)), 5):
        s.cell(row=i, column=13, value=p)
        s.cell(row=i, column=14, value=f"=COUNTIF($D$5:$D$60,M{i})")
        s.cell(row=i, column=15, value=f"=IF(SUM($N$5:$N$8)=0,\"\",N{i}/SUM($N$5:$N$8))").number_format = "0%"
        s.cell(row=i, column=16, value=target).number_format = "0%"
    s.column_dimensions["M"].width, s.column_dimensions["L"].width = 18, 3

    e = wb.create_sheet("Example")
    head(e, cols, widths)
    from datetime import date
    ex = [
        (date(2026, 12, 1), "Instagram", "Carousel", "Grooming tips", "Summer clips: what's safe for your breed?", "Thinking of shaving your dog for summer? Read this first.",
         "Save this", "#DogGroomingGeelong #GeelongDogs", "Slide 1: a fluffy dog in the shade with the title text", "Drafted", ""),
        (date(2026, 12, 3), "Instagram", "Reel", "Behind the scenes", "15 seconds of a calm bath", "This is what a calm groom looks like 🛁",
         "Follow for more", "#CageFreeGrooming #GeelongDogs", "", "Idea", ""),
        (date(2026, 12, 5), "Facebook", "Photo", "Happy dogs", "Before and after: Luna the shih tzu", "Luna came in looking like a mop…",
         "Book via link", "#ShihTzu #GeelongDogs", "Luna the shih tzu before and after her summer clip, side by side", "Scheduled",
         "https://baysidepaws.example/book?utm_source=facebook&utm_medium=social&utm_campaign=summer-dec"),
        (date(2026, 12, 4), "Instagram", "Story", "Offers & news", "Walk-in nail trims this Saturday, 8–12", "Nails clicking on the floor?",
         "Tap the link sticker", "", "Graphic: 'Walk-in nail trims, Saturday 8–12'", "Idea", ""),
    ]
    for r, row in enumerate(sorted(ex), 2):
        for c, v in enumerate(row, 1):
            cell = e.cell(row=r, column=c, value=v)
            cell.alignment = WRAP
            if c == 1:
                cell.number_format = "ddd d mmm"
    wb.calculation.fullCalcOnLoad = True
    wb.save(os.path.join(BUILD, "Social-Media-Content-Calendar.xlsx"))


# ---------------------------------------------------------------- Word templates
DNAVY, DCORAL, DGREY = RGBColor(0x1D, 0x2B, 0x4F), RGBColor(0xE8, 0x5D, 0x4A), RGBColor(0x56, 0x60, 0x7A)


def new_doc():
    doc = Document()
    sec = doc.sections[0]
    sec.page_height, sec.page_width = Cm(29.7), Cm(21.0)
    sec.top_margin = sec.bottom_margin = Cm(1.8)
    sec.left_margin = sec.right_margin = Cm(2.0)
    st = doc.styles["Normal"]
    st.font.name, st.font.size = "Calibri", Pt(10.5)
    st.paragraph_format.space_after = Pt(4)
    return doc


def shade(cell, hex_):
    tc = cell._tc.get_or_add_tcPr()
    s = OxmlElement("w:shd")
    s.set(qn("w:val"), "clear"); s.set(qn("w:color"), "auto"); s.set(qn("w:fill"), hex_)
    tc.append(s)


def para(doc, text, size=10.5, bold=False, color=None, italic=False, after=4):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(after)
    r = p.add_run(text)
    r.font.size, r.bold, r.italic = Pt(size), bold, italic
    if color:
        r.font.color.rgb = color
    return p


def h(doc, text):
    para(doc, text, 13, True, DCORAL, after=2)


def h3(doc, text):
    para(doc, text, 11, True, DNAVY, after=1)


def guide(doc, text):
    para(doc, text, 9.5, italic=True, color=DGREY)


def table(doc, header, rows, widths, side=False):
    t = doc.add_table(rows=1 if header else 0, cols=len(widths))
    t.style = "Table Grid"
    t.autofit = False
    if header:
        for i, txt in enumerate(header):
            c = t.rows[0].cells[i]
            c.paragraphs[0].add_run(txt).bold = True
            c.paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
            shade(c, "1D2B4F")
    for row in rows:
        cells = t.add_row().cells
        for i, txt in enumerate(row):
            r = cells[i].paragraphs[0].add_run(txt)
            if txt.startswith("["):
                r.font.color.rgb = DGREY
            if side and i == 0:
                r.bold = True
                shade(cells[0], "FFF6D6")
    for col, w in zip(t.columns, widths):
        col.width = Cm(w)
        for c in col.cells:
            c.width = Cm(w)
            for p in c.paragraphs:
                p.paragraph_format.space_after = Pt(1)
                for r in p.runs:
                    r.font.size = Pt(9.5)
    para(doc, "", after=2)
    return t


def plan_template():
    doc = new_doc()
    para(doc, "30-day social media plan: [Business name]", 20, True, DNAVY, after=2)
    para(doc, "[Dates covered] · Prepared by [your name] for [owner] · [Date]", 10, color=DGREY, after=10)
    guide(doc, "Grey text in square brackets is guidance: replace or delete it. Base the plan on what the data showed (Module 6), "
               "and keep it realistic for a busy owner: about an hour a week plus daily replies.")

    h(doc, "1. Goals")
    guide(doc, "1–3 SMART goals: specific, measurable, achievable, relevant, time-bound. Example: \"Get 10 puppy intro groom bookings "
               "from Instagram and Facebook in the next 30 days.\"")
    table(doc, ["Goal (SMART)", "Business goal it serves", "How we'll measure it"], [("1. ", "", ""), ("2. ", "", ""), ("3. ", "", "")], [7.0, 4.6, 5.4])

    h(doc, "2. Audience")
    guide(doc, "Two short profiles: who they are, what they care about, what worries them, when they're online. Example: Busy Sarah, 34, "
               "Newtown, two-year-old cavoodle, scrolls Instagram on the train and in the evening, worries about noisy salons.")
    for i in (1, 2):
        table(doc, None, [(f"Profile {i}: name, age, suburb", ""), ("Their dog / situation", ""), ("Cares about", ""), ("Worries about", ""),
                          ("When and where they're online", "")], [5.2, 11.8], side=True)

    h(doc, "3. Platforms")
    table(doc, ["Platform", "Why this one", "How often", "Formats"],
          [("[Instagram]", "[Where local dog owners are; Reels reach new people]", "[3 feed posts a week + stories]", "[Reels, carousels, stories]"),
           ("", "", "", ""), ("", "", "", "")], [3.2, 6.2, 3.8, 3.8])

    h(doc, "4. Content pillars")
    table(doc, ["Pillar", "Share of posts", "Why", "Example posts"],
          [("[Grooming tips]", "[30%]", "[Shows expertise; gets saved]", "[How often to groom]"), ("", "", "", ""), ("", "", "", ""), ("", "", "", "")],
          [3.6, 2.4, 5.0, 6.0])

    h(doc, "5. 30-day content calendar")
    guide(doc, "Fill in the content calendar template (Social-Media-Content-Calendar.xlsx) and attach it, or paste the first two weeks here.")
    para(doc, "[Attached / pasted]")

    h(doc, "6. Four sample posts")
    guide(doc, "Finished posts: the image or video idea (you can adapt the brand kit graphics), the caption with hook, value and CTA, "
               "3–5 hashtags in CamelCase, and alt text. Check each one against the post checklist.")
    for i in range(1, 5):
        h3(doc, f"Post {i}")
        table(doc, None, [("Pillar, format, platform, date", ""), ("Image or video idea", ""), ("Caption: hook", ""), ("Caption: value", ""),
                          ("Caption: call to action", ""), ("Hashtags", ""), ("Alt text", "")], [5.2, 11.8], side=True)

    h(doc, "7. Community and customer care")
    table(doc, None, [("Reply times", "[e.g. comments and messages within 1 working day]"), ("Who replies, and when", ""),
                      ("How complaints are handled", "[Reply in public calmly, take details to a private message, follow up]")], [5.2, 11.8], side=True)
    h3(doc, "Three saved replies")
    for i in range(1, 4):
        para(doc, f"{i}. [Question] → [Reply in our voice]", after=1)
    para(doc, "", after=2)

    h(doc, "8. Optional: paid boost")
    table(doc, None, [("Post to boost", ""), ("Goal", ""), ("Audience (place, age 18+, interests)", ""), ("Budget and length", "[e.g. $70 over 7 days]"),
                      ("How we'll judge success", "")], [5.2, 11.8], side=True)

    h(doc, "9. Measurement")
    table(doc, ["Goal", "Numbers we'll track", "Where we'll find them", "How often"],
          [("1.", "", "", ""), ("2.", "", "", ""), ("3.", "", "", "")], [2.0, 5.4, 5.6, 4.0])
    para(doc, "Bio link with UTM tags: [https://baysidepaws.example/book?utm_source=instagram&utm_medium=social&utm_campaign=bio]", 9.5)
    para(doc, "And ask every new customer: \"How did you hear about us?\"", 9.5, italic=True)
    para(doc, "Practice business: Bayside Paws Dog Grooming is made up, for Avro Academy's Social Media Marketing course.", 8.5, italic=True, color=DGREY)
    doc.save(os.path.join(BUILD, "Social-Media-Plan-Template.docx"))


def monthly_template():
    doc = new_doc()
    para(doc, "Social media report: [Month Year]", 20, True, DNAVY, after=2)
    para(doc, "[Business name] · Prepared by [your name] for [owner]", 10, color=DGREY, after=10)
    guide(doc, "Grey text in square brackets is guidance: replace or delete it. Lead with business results (bookings, messages, calls), "
               "then the social numbers. Explain, don't just list. Be honest about a slow month, and never promise follower or sales numbers.")

    h(doc, "Summary")
    guide(doc, "3 sentences: the headline result, what worked, what's next. Example: \"In September, Instagram and Facebook brought 8 bookings "
               "(up from 4 in August) and 365 link clicks. Our puppy-groom offer and Archie the spoodle's before-and-after did best. In October "
               "we'll post two Reels a week, keep one tip carousel a week, and run a $70 boost on the puppy offer.\"")
    para(doc, "[Your summary]")

    h(doc, "Results vs last month")
    table(doc, ["Measure", "This month", "Last month", "Change"],
          [("Bookings from social (\"How did you hear about us?\")", "", "", ""), ("Messages and calls from social", "", "", ""),
           ("Link clicks", "", "", ""), ("Reach", "", "", ""), ("Average engagement rate", "", "", ""), ("Followers (end of month)", "", "", ""),
           ("Posts published", "", "", "")], [8.0, 3.0, 3.0, 3.0])
    guide(doc, "Engagement rate = (likes + comments + shares + saves) ÷ reach. Find the numbers in Meta Business Suite → Insights.")

    h(doc, "Top 3 posts, and why they worked")
    table(doc, ["Post", "Format and pillar", "Result", "Why it worked"],
          [("1. [Archie the spoodle: before and after]", "[Reel, Happy dogs]", "[2 bookings, 1,9xx reach]", "[A real result, hook in the first second]"),
           ("2.", "", "", ""), ("3.", "", "", "")], [4.8, 3.4, 3.4, 5.4])

    h(doc, "What we learned")
    guide(doc, "2–3 points, in plain words: \"Reels reached twice as many people as photos.\"")
    for _ in range(3):
        para(doc, "• [ ]", after=1)

    h(doc, "Next month's plan")
    guide(doc, "3 specific actions.")
    for i in range(1, 4):
        para(doc, f"{i}. [ ]", after=1)
    doc.save(os.path.join(BUILD, "Monthly-Social-Media-Report-Template.docx"))


if __name__ == "__main__":
    practice_workbook()
    calendar_workbook()
    plan_template()
    monthly_template()
    print("built into", os.path.abspath(BUILD))
