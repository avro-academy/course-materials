"""Builds the SEO Basics templates into ../build:
Keyword-Research-Template.xlsx, SEO-Audit-Template.xlsx,
SEO-Audit-Report-Template.docx, Monthly-SEO-Report-Template.docx."""
import os

from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import CellIsRule, FormulaRule

BUILD = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "build")
os.makedirs(BUILD, exist_ok=True)

NAVY = PatternFill("solid", fgColor="1D2B4F")
YEL = PatternFill("solid", fgColor="FFF6D6")
RED = PatternFill("solid", fgColor="FBD5D0")
AMBER = PatternFill("solid", fgColor="FFE9B8")
GREEN = PatternFill("solid", fgColor="D5F0E3")
WHITE = Font(color="FFFFFF", bold=True)
TITLE = Font(bold=True, size=14, color="1D2B4F")
NOTE = Font(italic=True, color="56607A")
WRAP = Alignment(wrap_text=True, vertical="top")


def head(ws, cols, widths, row=1):
    for i, (c, w) in enumerate(zip(cols, widths), 1):
        cell = ws.cell(row=row, column=i, value=c)
        cell.fill, cell.font, cell.alignment = NAVY, WHITE, Alignment(wrap_text=True, vertical="center")
        ws.column_dimensions[cell.column_letter].width = w
    ws.freeze_panes = ws.cell(row=row + 1, column=1)


def notes(ws, lines, start=1):
    ws.cell(row=start, column=1, value=lines[0]).font = TITLE
    for i, t in enumerate(lines[1:], start + 1):
        ws.cell(row=i, column=1, value=t).alignment = WRAP
    ws.column_dimensions["A"].width = 110


def pick(ws, rng, options, prompt):
    dv = DataValidation(type="list", formula1='"' + ",".join(options) + '"', allow_blank=True)
    dv.promptTitle, dv.prompt = "Choose one", prompt
    ws.add_data_validation(dv)
    dv.add(rng)


# ---------------------------------------------------------------- keyword research
KW_COLS = ["Keyword", "Search intent", "Monthly searches (rough)", "Competition", "Who ranks now?", "Target page", "Status", "Notes"]
KW_W = [36, 16, 14, 13, 34, 30, 14, 34]
INTENTS = ["Informational", "Commercial", "Transactional", "Navigational"]
EXAMPLE = [
    ("dog grooming geelong", "Transactional", "100–1K", "Medium", "Map pack, 2 local groomers, a directory", "Home (index.html)", "Targeted", "Main keyword for the home page"),
    ("dog groomer geelong west", "Transactional", "10–100", "Low", "Map pack, small local sites", "Home (index.html)", "Targeted", "Suburb version, same page"),
    ("dog grooming prices geelong", "Commercial", "10–100", "Low", "Local groomers' price pages", "Prices (prices.html)", "Targeted", "Prices must be text, not an image"),
    ("dog nail trim geelong", "Transactional", "10–100", "Low", "Vets and groomers", "Services (services.html#nails)", "Targeted", ""),
    ("puppy groom", "Commercial", "100–1K", "Medium", "National pet chains, guides", "Services (services.html#puppy)", "Targeted", "Later: its own page (content plan)"),
    ("how often should I groom my dog", "Informational", "1K–10K", "High", "Pet blogs, vet clinics", "Blog post", "Targeted", "Answer in the first sentence"),
    ("bayside paws", "Navigational", "10–100", "Low", "Our site, our profile", "Home (index.html)", "Targeted", ""),
    ("summer dog clip", "Informational", "100–1K", "Medium", "Pet blogs", "(none yet)", "Content idea", "Publish in December"),
]


def keyword_workbook():
    wb = Workbook()
    ws = wb.active
    ws.title = "How to use"
    notes(ws, [
        "Keyword research template",
        "A keyword map matches each keyword to the ONE page that should rank for it. (SEO Basics, Module 2.)",
        "",
        "1. Find keywords with Google autocomplete, People also ask, related searches, Google Trends and Keyword Planner.",
        "2. On the Keyword map sheet, add one row per keyword. Choose its search intent from the list.",
        "3. Monthly searches: a rough range from Keyword Planner, such as 10–100 or 100–1K. Leave it blank if you can't find one.",
        "4. Competition: search the keyword. Big national brands and directories = High. Small local sites = Low (winnable).",
        "5. Target page: the one page on the site that should rank. One main keyword per page, and one page per main keyword.",
        "6. Match the intent: informational keywords go to guides or blog posts; transactional ones to service or booking pages.",
        "7. No page for a keyword yet? Put \"(none yet)\" and status \"Content idea\". That's your content plan (Module 6).",
        "",
        "The Bayside Paws example sheet shows a finished map for the practice site.",
        "Pages that appear twice as a target are highlighted on the Keyword map: check they aren't competing for the same main keyword.",
    ])
    for name, rows in (("Keyword map", []), ("Bayside Paws example", EXAMPLE)):
        s = wb.create_sheet(name)
        head(s, KW_COLS, KW_W)
        for r, row in enumerate(rows, 2):
            for c, v in enumerate(row, 1):
                s.cell(row=r, column=c, value=v).alignment = WRAP
        last = 101
        pick(s, f"B2:B{last}", INTENTS, "What does the searcher want to do?")
        pick(s, f"D2:D{last}", ["Low", "Medium", "High"], "Who ranks now? Big brands = High, small local sites = Low.")
        pick(s, f"G2:G{last}", ["Targeted", "To do", "Content idea"], "Is a page already targeting it?")
        s.conditional_formatting.add(f"A2:A{last}", FormulaRule(formula=[f'COUNTIF($A$2:$A${last},A2)>1'], fill=RED))
        if name == "Keyword map":
            s.conditional_formatting.add(f"F2:F{last}", FormulaRule(formula=[f'AND(F2<>"",COUNTIF($F$2:$F${last},F2)>1)'], fill=AMBER))
            for r in range(2, 32):
                for c in range(1, 9):
                    s.cell(row=r, column=c).fill = YEL if c in (1, 2, 6) else PatternFill()
    wb.save(os.path.join(BUILD, "Keyword-Research-Template.xlsx"))


# ---------------------------------------------------------------- audit workbook
def audit_workbook():
    wb = Workbook()
    ws = wb.active
    ws.title = "Start here"
    notes(ws, [
        "SEO audit template",
        "For the SEO Basics final project: audit the Bayside Paws \"before\" site (or a real client's site) and plan the fixes.",
        "",
        "Page checks: one row per page. Paste the title and meta description; the lengths and checks work themselves out.",
        "Issues: every problem you find, with its area, priority and fix. Sort by priority, quick high-impact fixes first.",
        "Scores: SEO Lab and PageSpeed Insights (mobile) results before and after your fixes.",
        "30-day plan: week by week, specific actions and who does them.",
        "",
        "Priority: High = stops people or Google finding/using the page (no viewport, broken links, prices in an image, wrong phone number).",
        "Medium = makes results weaker (vague titles, missing alt text, big images). Low = nice to have.",
        "The practice site has 15+ planted issues. Compare with the fixed folder when you're done.",
    ])

    s = wb.create_sheet("Page checks")
    cols = ["Page", "URL", "Title tag", "Title length", "Title check", "Meta description", "Description length", "Description check",
            "Number of H1s", "H1 text", "Main keyword (from your map)", "Keyword in title?", "Images", "Images missing alt", "Broken or vague links",
            "Viewport tag?", "Notes"]
    head(s, cols, [14, 30, 40, 8, 16, 46, 10, 18, 8, 30, 26, 10, 8, 10, 26, 10, 36])
    pages = ["Home", "Services", "Prices", "About", "Contact", "Blog post"]
    for r in range(2, 32):
        if r - 2 < len(pages):
            s.cell(row=r, column=1, value=pages[r - 2])
        s.cell(row=r, column=4, value=f'=IF(C{r}="","",LEN(C{r}))')
        s.cell(row=r, column=5, value=f'=IF(C{r}="","",IF(D{r}<30,"Too short",IF(D{r}>60,"May be cut off","Good")))')
        s.cell(row=r, column=7, value=f'=IF(F{r}="","",LEN(F{r}))')
        s.cell(row=r, column=8, value=f'=IF(AND(C{r}="",F{r}=""),"",IF(F{r}="","Missing",IF(G{r}<120,"Too short",IF(G{r}>160,"May be cut off","Good"))))')
        s.cell(row=r, column=12, value=f'=IF(OR(C{r}="",K{r}=""),"",IF(ISNUMBER(SEARCH(K{r},C{r})),"Yes","No"))')
        for c in (3, 6, 10, 15, 17):
            s.cell(row=r, column=c).alignment = WRAP
    pick(s, "P2:P31", ["Yes", "No"], "Is <meta name=\"viewport\"> in the <head>?")
    for col in ("E", "H"):
        s.conditional_formatting.add(f"{col}2:{col}31", CellIsRule(operator="equal", formula=['"Good"'], fill=GREEN))
        s.conditional_formatting.add(f"{col}2:{col}31", FormulaRule(formula=[f'AND({col}2<>"",{col}2<>"Good")'], fill=AMBER))
    s.conditional_formatting.add("I2:I31", FormulaRule(formula=['AND(I2<>"",I2<>1)'], fill=RED))
    s.conditional_formatting.add("L2:L31", CellIsRule(operator="equal", formula=['"No"'], fill=AMBER))
    s.conditional_formatting.add("N2:N31", CellIsRule(operator="greaterThan", formula=["0"], fill=AMBER))
    s.conditional_formatting.add("P2:P31", CellIsRule(operator="equal", formula=['"No"'], fill=RED))

    s = wb.create_sheet("Issues")
    head(s, ["#", "Page", "Area", "Issue", "Why it matters", "Fix", "Priority", "Effort", "Status", "Date fixed"],
         [5, 14, 13, 40, 36, 40, 10, 10, 12, 12])
    examples = [
        ("Home", "On-page", "Title is just \"Home\"", "The title is the blue link in Google; \"Home\" says nothing about the business",
         "Dog Grooming Geelong | Bayside Paws Dog Grooming", "High", "Quick", "To do"),
        ("All pages", "Technical", "No viewport tag", "Text is tiny on phones; Google ranks the mobile version",
         "Add <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">", "High", "Quick", "To do"),
    ]
    for r in range(2, 62):
        s.cell(row=r, column=1, value=r - 1)
        for c in (4, 5, 6):
            s.cell(row=r, column=c).alignment = WRAP
    for r, row in enumerate(examples, 2):
        for c, v in enumerate(row, 2):
            s.cell(row=r, column=c, value=v).alignment = WRAP
    s.cell(row=2, column=1).comment = None
    pick(s, "C2:C61", ["On-page", "Content", "Images", "Links", "Technical", "Speed", "Local", "Reviews"], "Which area is it?")
    pick(s, "G2:G61", ["High", "Medium", "Low"], "Impact on customers and on Google")
    pick(s, "H2:H61", ["Quick", "Medium", "Big"], "How much work is the fix?")
    pick(s, "I2:I61", ["To do", "Doing", "Done", "Won't fix"], "Where is it up to?")
    s.conditional_formatting.add("G2:G61", CellIsRule(operator="equal", formula=['"High"'], fill=RED))
    s.conditional_formatting.add("G2:G61", CellIsRule(operator="equal", formula=['"Medium"'], fill=AMBER))
    s.conditional_formatting.add("I2:I61", CellIsRule(operator="equal", formula=['"Done"'], fill=GREEN))
    s.auto_filter.ref = "A1:J61"
    s["L1"], s["L2"], s["L3"], s["L4"], s["L5"] = "Summary", "High, not done", "Medium, not done", "Low, not done", "Done"
    s["L1"].font = Font(bold=True)
    s["M2"] = '=COUNTIFS(G2:G61,"High",I2:I61,"<>Done")'
    s["M3"] = '=COUNTIFS(G2:G61,"Medium",I2:I61,"<>Done")'
    s["M4"] = '=COUNTIFS(G2:G61,"Low",I2:I61,"<>Done")'
    s["M5"] = '=COUNTIF(I2:I61,"Done")'
    s.column_dimensions["L"].width = 18

    s = wb.create_sheet("Scores")
    head(s, ["Check", "Page", "Before", "After", "Change", "Notes"], [34, 16, 12, 12, 12, 40])
    checks = [("SEO Lab page checker score", "Home"), ("SEO Lab page checker score", "Services"), ("SEO Lab page checker score", "Prices"),
              ("SEO Lab whole-site check: issues found", "Whole site"), ("PageSpeed Insights mobile: Performance", "Home"),
              ("PageSpeed Insights mobile: LCP (seconds)", "Home"), ("PageSpeed Insights mobile: CLS", "Home"),
              ("PageSpeed Insights mobile: SEO score", "Home"), ("PageSpeed Insights mobile: Accessibility", "Home"),
              ("Pages indexed (Search Console)", "Whole site")]
    for r, (a, b) in enumerate(checks, 2):
        s.cell(row=r, column=1, value=a)
        s.cell(row=r, column=2, value=b)
        s.cell(row=r, column=5, value=f'=IF(OR(C{r}="",D{r}=""),"",D{r}-C{r})')
    s.cell(row=13, column=1, value="LCP: 2.5 s or less is good. CLS: 0.1 or less is good. For LCP and CLS, lower is better.").font = NOTE

    s = wb.create_sheet("30-day plan")
    head(s, ["Week", "Action", "Issue #s", "Who", "Done?"], [8, 60, 10, 16, 10])
    plan = [(1, "Fix titles, descriptions and H1s on all pages; add the viewport tag; fix the broken map link"),
            (2, "Replace the prices image with a table; compress and rename images; add alt text; consistent NAP in the footer"),
            (3, "Rewrite the blog post to answer the question; set up Search Console and submit the sitemap; add structured data"),
            (4, "Claim and complete Google Business Profile; start asking every customer for a review; list on 3 key directories")]
    r = 2
    for week, example in plan:
        s.cell(row=r, column=1, value=week)
        s.cell(row=r, column=2, value="[Example] " + example).font = NOTE
        s.cell(row=r, column=2).alignment = WRAP
        r += 4
    pick(s, "E2:E40", ["Yes", "No"], "Done?")
    wb.calculation.fullCalcOnLoad = True
    wb.save(os.path.join(BUILD, "SEO-Audit-Template.xlsx"))


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


def guide(doc, text):
    para(doc, text, 9.5, italic=True, color=DGREY)


def table(doc, header, rows, widths):
    t = doc.add_table(rows=1, cols=len(header))
    t.style = "Table Grid"
    t.autofit = False
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


def audit_report():
    doc = new_doc()
    para(doc, "SEO audit: [Business name]", 20, True, DNAVY, after=2)
    para(doc, "[Website address] · Prepared by [your name] · [Date]", 10, color=DGREY, after=10)
    guide(doc, "Grey text in square brackets is guidance: replace or delete it. Keep the report to 2–4 pages, in plain language. "
               "Lead with what matters to the business: customers finding them and getting in touch.")

    h(doc, "1. Summary")
    guide(doc, "3–4 sentences: how the site is doing now, the most important problems, and what fixing them will do. For example: "
               "\"The site is hard to find for local searches and hard to use on a phone. Every page has a generic title, the prices are "
               "a picture Google can't read, and the phone number differs between pages. The top 5 fixes take about a day and should "
               "help more Geelong dog owners find and call the salon.\"")
    para(doc, "[Your summary]")

    h(doc, "2. Top issues")
    guide(doc, "The 5–8 most important issues from your audit spreadsheet, highest priority first.")
    table(doc, ["#", "Issue", "Why it matters", "Fix", "Priority"],
          [("1", "[Example: titles are \"Home\", \"Prices\", \"Post\"]", "[Titles are the blue link in Google]", "[Unique titles with the keyword]", "[High]")]
          + [(str(i), "", "", "", "") for i in range(2, 9)], [0.8, 4.6, 4.4, 4.6, 1.8])

    h(doc, "3. Keyword map")
    guide(doc, "One main keyword per page, matched to the searcher's intent. Include keywords with no page yet as content ideas.")
    table(doc, ["Keyword", "Intent", "Target page"],
          [("[dog grooming geelong]", "[Transactional]", "[Home]")] + [("", "", "")] * 7, [7.2, 3.6, 5.4])

    h(doc, "4. Local SEO")
    para(doc, "Business details to use everywhere (NAP)", 11, True, DNAVY, after=1)
    guide(doc, "One exact version of the name, address and phone. Use it in the site footer, on the Contact page, on Google Business Profile and in every directory.")
    para(doc, "[Business name]\n[Street address, suburb, state, postcode]\n[Phone]")
    para(doc, "Google Business Profile checklist", 11, True, DNAVY, after=1)
    for item in ["Claimed and verified by the owner", "Primary category: [most specific, e.g. Dog groomer]", "Hours, including holiday hours",
                 "Phone and website link", "Services with descriptions and prices", "Description written for customers (up to 750 characters)",
                 "Real photos: shopfront, inside, team, work", "A plan to ask every customer for a review, and reply to every review"]:
        para(doc, "☐ " + item, after=1)
    para(doc, "", after=2)
    para(doc, "Five honest link ideas", 11, True, DNAVY, after=1)
    table(doc, ["Who to contact", "What we'd offer them"], [("[Example: a local vet clinic]", "[A grooming tips sheet for their clients; a link to our site]")]
          + [("", "")] * 4, [6.2, 10.0])

    h(doc, "5. 30-day plan")
    table(doc, ["Week", "Actions", "Who"],
          [("1", "[Fix titles, descriptions and H1s on all pages; add the viewport tag; fix the broken map link]", ""),
           ("2", "[Replace the prices image with a table; compress and rename images; add alt text; consistent NAP in the footer]", ""),
           ("3", "[Rewrite the blog post to answer the question; set up Search Console and submit the sitemap; add structured data]", ""),
           ("4", "[Claim and complete Google Business Profile; ask every customer for a review; list on 3 key directories]", "")],
          [1.4, 11.8, 3.0])

    h(doc, "6. Before and after")
    guide(doc, "After applying at least your top 5 fixes, test again. Explain what changed in one or two sentences.")
    table(doc, ["Check", "Before", "After"],
          [("SEO Lab page checker: Home", "", ""), ("SEO Lab whole-site check: issues found", "", ""),
           ("PageSpeed Insights mobile: Performance", "", ""), ("PageSpeed Insights mobile: LCP", "", ""),
           ("Pages indexed in Search Console", "", "")], [8.2, 4.0, 4.0])
    para(doc, "[What changed, and what you'd do next]")
    para(doc, "Practice site: Bayside Paws Dog Grooming is a made-up business used in Avro Academy's SEO Basics course.", 8.5, italic=True, color=DGREY)
    doc.save(os.path.join(BUILD, "SEO-Audit-Report-Template.docx"))


def monthly_report():
    doc = new_doc()
    para(doc, "SEO report: [Month Year]", 20, True, DNAVY, after=2)
    para(doc, "[Business name] · [Website address] · Prepared by [your name] for [client or manager]", 10, color=DGREY, after=10)
    guide(doc, "Grey text in square brackets is guidance: replace or delete it. Use plain language, be honest about slow months, "
               "and never promise rankings.")

    h(doc, "Summary")
    guide(doc, "3 sentences: the headline result, what you did, what's next. Example: \"In November, Google searches brought 312 visits "
               "to the site (up 24% on October) and 18 calls from the Business Profile. We fixed titles and descriptions on all six pages "
               "and published the new grooming-frequency guide, which now appears for 40 searches. In December we'll add the puppy "
               "grooming page and ask every customer for a review.\"")
    para(doc, "[Your summary]")

    h(doc, "Results")
    guide(doc, "Lead with customers: calls, bookings and enquiries from search. From Search Console, Google Analytics (Organic Search) "
               "and Google Business Profile Performance.")
    table(doc, ["Measure", "This month", "Last month", "Change", "Same month last year"],
          [("Calls from Google Business Profile", "", "", "", ""), ("Bookings or enquiries from search (GA4 key events)", "", "", "", ""),
           ("Direction requests", "", "", "", ""), ("Organic visits (GA4 Organic Search)", "", "", "", ""),
           ("Clicks from Google (Search Console)", "", "", "", ""), ("Impressions (Search Console)", "", "", "", ""),
           ("Average position (Search Console)", "", "", "", "")], [6.6, 2.4, 2.4, 2.2, 2.6])

    h(doc, "Top searches and pages")
    table(doc, ["Top searches (Search Console > Queries)", "Clicks", "Impressions", "Position"],
          [("[dog grooming geelong]", "", "", "")] + [("", "", "", "")] * 4, [8.6, 2.4, 2.8, 2.4])
    table(doc, ["Top pages (Search Console > Pages)", "Clicks", "Impressions"],
          [("[/prices.html]", "", "")] + [("", "", "")] * 4, [11.0, 2.4, 2.8])

    h(doc, "Work done this month")
    guide(doc, "Pages fixed, content published, reviews replied to, listings updated. Be specific.")
    for _ in range(4):
        para(doc, "• [ ]", after=1)

    h(doc, "Issues found")
    guide(doc, "Errors in Search Console (Pages report), broken links, speed problems, anything that needs the client's help.")
    for _ in range(3):
        para(doc, "• [ ]", after=1)

    h(doc, "Next month's plan")
    guide(doc, "3–5 specific actions.")
    for i in range(1, 6):
        para(doc, f"{i}. [ ]", after=1)
    doc.save(os.path.join(BUILD, "Monthly-SEO-Report-Template.docx"))


if __name__ == "__main__":
    keyword_workbook()
    audit_workbook()
    audit_report()
    monthly_report()
    print("built into", os.path.abspath(BUILD))
