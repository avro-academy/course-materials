"""Builds IT-Spending-Policy-Template.docx (one page) into ../build."""
import os
from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "build", "IT-Spending-Policy-Template.docx")
NAVY, CORAL, GREY = RGBColor(0x1D, 0x2B, 0x4F), RGBColor(0xE8, 0x5D, 0x4A), RGBColor(0x56, 0x60, 0x7A)

doc = Document()
sec = doc.sections[0]
sec.page_height, sec.page_width = Cm(29.7), Cm(21.0)
sec.top_margin = sec.bottom_margin = Cm(1.5)
sec.left_margin = sec.right_margin = Cm(1.8)
st = doc.styles["Normal"]
st.font.name, st.font.size = "Calibri", Pt(10)
st.paragraph_format.space_after = Pt(3)


def shade(cell, hex_):
    tc = cell._tc.get_or_add_tcPr()
    s = OxmlElement("w:shd"); s.set(qn("w:val"), "clear"); s.set(qn("w:color"), "auto"); s.set(qn("w:fill"), hex_)
    tc.append(s)


def para(text, size=10, bold=False, color=None, italic=False, after=3):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(after)
    r = p.add_run(text); r.font.size = Pt(size); r.bold = bold; r.italic = italic
    if color: r.font.color.rgb = color
    return p


para("[Business name] — IT spending policy", 18, True, NAVY, after=2)
para("Version [1.0] · Approved by [name, role] on [date] · Next review [date] · Questions: [IT coordinator, email]", 9, color=GREY, after=6)
para("Why we have this policy", 12, True, CORAL, after=1)
para("So we know every tool and device we pay for, don't pay for the same thing twice, keep client and personal information safe, "
     "and can plan next year's budget. It should never slow down real work: most requests are answered within [2] working days.")

para("The rules", 12, True, CORAL, after=1)
rules = [
    ("Ask before you buy", "Any new software, subscription or device goes through the request form ([link]): what it's for, who needs it, "
     "what it costs per month, and whether it will hold client or personal information."),
    ("Approval limits", "Under $[100] a month: the tool's owner or the IT coordinator. $[100]–$[2,000]: [studio/office manager]. "
     "Over $[2,000], or any annual contract or lease: [director/owner], with [3] written quotes."),
    ("One register", "Every subscription and device is added to the subscription register or asset register, with an owner, before it's paid for."),
    ("Company accounts only", "Tools are signed up with a work email and paid on a company card, so they stay with the business when people leave. "
     "No personal accounts for work data."),
    ("Check the data", "Before client files or personal information go into a new tool (including AI tools), the IT coordinator checks where the "
     "data is stored, who can see it and whether it's used for training. Never put [list: e.g. client passwords, health or payment details] into AI tools."),
    ("Starters and leavers", "Seats are added and removed only through the onboarding and offboarding checklists. Managers tell [IT coordinator] "
     "about every leaver at least [5] working days before their last day."),
    ("Renewals", "Every renewal date is in the shared calendar. [60] days before, the owner checks seats in use, the price and whether we still need it."),
    ("Reviews", "Monthly: the IT coordinator checks the statement for new or changed charges. Yearly: a full review of the registers and the budget."),
]
t = doc.add_table(rows=0, cols=2)
t.alignment = WD_TABLE_ALIGNMENT.CENTER
t.style = "Table Grid"
for i, (a, b) in enumerate(rules):
    row = t.add_row().cells
    row[0].width, row[1].width = Cm(4.2), Cm(13.2)
    row[0].paragraphs[0].add_run(a).bold = True
    row[1].paragraphs[0].add_run(b)
    for c in row:
        c.paragraphs[0].paragraph_format.space_after = Pt(1)
        for r in c.paragraphs[0].runs: r.font.size = Pt(9.5)
    if i % 2 == 0:
        shade(row[0], "FFF6D6"); shade(row[1], "FFF6D6")

t.autofit = False
for col, w in zip(t.columns, (Cm(4.2), Cm(13.2))):
    col.width = w
    for c in col.cells: c.width = w
para("", after=2)
para("Owners", 12, True, CORAL, after=1)
para("Every tool has an owner who approves changes, knows who uses it and checks it before renewal. The owners are listed in the "
     "subscription register ([link]).")
para("If something goes wrong", 12, True, CORAL, after=1)
para("Bought something without asking? Found a tool nobody listed? Tell [IT coordinator] straight away. Nobody is in trouble for asking or "
     "owning up — we just want to know what we have.")
para("Tip: keep it to one page. Replace everything in [square brackets], delete what doesn't fit your business, and explain the why when you share it.",
     8.5, italic=True, color=GREY, after=0)
doc.save(OUT)
print("saved", OUT)
