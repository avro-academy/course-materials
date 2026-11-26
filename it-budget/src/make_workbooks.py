"""Builds Brightline-IT-Costs.xlsx (the worked example) and IT-Cost-Templates.xlsx (empty) into ../build.

Every number in the course comes from formulas in these sheets. Run: python make_workbooks.py
"""
import datetime as dt
import os
import random

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.worksheet.datavalidation import DataValidation

BUILD = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "build")
NAVY = PatternFill("solid", fgColor="1D2B4F")
YEL = PatternFill("solid", fgColor="FFF6D6")
TOT = PatternFill("solid", fgColor="E8ECF4")
WHITE = Font(color="FFFFFF", bold=True)
BOLD = Font(bold=True)
NOTE = Font(italic=True, color="56607A")
TITLE = Font(bold=True, size=14, color="1D2B4F")
MONEY = '"$"#,##0.00'
MONEY0 = '"$"#,##0'
DATE = "d/mm/yyyy"
CATS = ["Software & cloud", "Hardware", "Internet & phones", "IT support & services", "Security & backup"]
D = dt.date


def head(ws, cols, widths, row=1):
    for i, (c, w) in enumerate(zip(cols, widths), 1):
        x = ws.cell(row=row, column=i, value=c)
        x.fill, x.font = NAVY, WHITE
        x.alignment = Alignment(wrap_text=True, vertical="center")
        ws.column_dimensions[x.column_letter].width = w
    ws.row_dimensions[row].height = 30
    ws.freeze_panes = ws.cell(row=row + 1, column=1)


def put(ws, ref, value, fmt=None, font=None, fill=None):
    c = ws[ref]
    c.value = value
    if fmt: c.number_format = fmt
    if font: c.font = font
    if fill: c.fill = fill
    return c


# ---------------------------------------------------------------- Brightline's data

STAFF = [  # name, role, started, laptop tag, left
    ("Maya Chen", "Creative director", D(2016, 2, 1), "BL-LAP-001", None),
    ("Hana Sato", "Studio manager", D(2018, 5, 14), "BL-LAP-011", None),
    ("Ethan Nguyen", "Finance", D(2019, 9, 2), "BL-LAP-005", None),
    ("Leo Martin", "Senior designer", D(2017, 3, 6), "BL-LAP-002", None),
    ("Priya Raman", "Designer", D(2021, 10, 25), "BL-LAP-003", None),
    ("Omar Haddad", "Account manager", D(2022, 2, 7), "BL-LAP-004", None),
    ("Tom Becker", "Designer", D(2022, 8, 15), "BL-LAP-008", None),
    ("Aisha Khan", "Designer", D(2022, 11, 1), "BL-LAP-009", None),
    ("Ben Walsh", "Motion designer", D(2023, 1, 9), "BL-LAP-010", None),
    ("Ruby Ellis", "Account manager", D(2023, 5, 22), "BL-LAP-012", None),
    ("Sam Taylor", "Designer", D(2024, 2, 5), "BL-LAP-013", None),
    ("Jordan Price", "Web developer", D(2024, 4, 8), "BL-LAP-014", None),
    ("Grace Liu", "Designer", D(2025, 9, 22), "BL-LAP-015", None),
    ("Chloe Dubois", "Account manager", D(2025, 10, 6), "BL-LAP-016", None),
    ("Alex Romero", "Junior designer", D(2025, 10, 13), "BL-LAP-017", None),
    ("Zoe Wright", "Designer", D(2020, 6, 1), "", D(2025, 9, 19)),
    ("Marcus Lee", "Designer", D(2019, 1, 14), "", D(2025, 12, 12)),
    ("Ella Brooks", "Account manager", D(2021, 4, 12), "", D(2026, 3, 27)),
]
ASSETS = [  # tag, type, assigned to, bought, price, warranty years
    ("BL-LAP-001", "Laptop", "Maya Chen", D(2021, 3, 8), 2399, 3),
    ("BL-LAP-002", "Laptop", "Leo Martin", D(2020, 8, 17), 2299, 3),
    ("BL-LAP-003", "Laptop", "Priya Raman", D(2021, 11, 2), 2399, 3),
    ("BL-LAP-004", "Laptop", "Omar Haddad", D(2022, 2, 14), 1899, 3),
    ("BL-LAP-005", "Laptop", "Ethan Nguyen", D(2020, 10, 5), 1799, 3),
    ("BL-LAP-006", "Laptop", "Spare (office)", D(2019, 3, 25), 1999, 1),
    ("BL-LAP-007", "Laptop", "Spare (office)", D(2020, 6, 10), 2099, 3),
    ("BL-LAP-008", "Laptop", "Tom Becker", D(2022, 8, 22), 2599, 3),
    ("BL-LAP-009", "Laptop", "Aisha Khan", D(2022, 11, 7), 2599, 3),
    ("BL-LAP-010", "Laptop", "Ben Walsh", D(2023, 1, 16), 2799, 3),
    ("BL-LAP-011", "Laptop", "Hana Sato", D(2023, 3, 6), 1999, 3),
    ("BL-LAP-012", "Laptop", "Ruby Ellis", D(2023, 5, 29), 1999, 3),
    ("BL-LAP-013", "Laptop", "Sam Taylor", D(2024, 2, 12), 2699, 3),
    ("BL-LAP-014", "Laptop", "Jordan Price", D(2024, 4, 15), 2699, 3),
    ("BL-LAP-015", "Laptop", "Grace Liu", D(2025, 9, 23), 2899, 3),
    ("BL-LAP-016", "Laptop", "Chloe Dubois", D(2025, 9, 23), 2899, 3),
    ("BL-LAP-017", "Laptop", "Alex Romero", D(2025, 9, 23), 2899, 3),
    ("BL-MON-001", "Monitor", "Leo Martin", D(2020, 8, 17), 429, 3),
    ("BL-MON-002", "Monitor", "Maya Chen", D(2020, 8, 17), 429, 3),
    ("BL-MON-003", "Monitor", "Priya Raman", D(2026, 2, 10), 549, 3),
    ("BL-MON-004", "Monitor", "Ben Walsh", D(2026, 2, 10), 549, 3),
    ("BL-NET-001", "Router", "Office", D(2019, 6, 3), 349, 1),
]
SUBS = [  # tool, plan, billing, owner, price per seat per month, seats paid, renews
    ("Microsoft 365", "Business Standard", "Monthly", "Hana Sato", 21, 18, D(2026, 7, 14)),
    ("Adobe Creative Cloud", "All Apps (teams)", "Annual", "Leo Martin", 89.99, 12, D(2026, 8, 4)),
    ("Figma", "Professional (editor seats)", "Annual", "Leo Martin", 24, 10, D(2027, 2, 16)),
    ("Canva", "Teams", "Annual", "Ruby Ellis", 40, 6, D(2026, 11, 9)),
    ("Zoom", "Pro", "Monthly", "Hana Sato", 23.99, 5, D(2026, 7, 21)),
    ("Slack", "Pro", "Monthly", "Hana Sato", 13.50, 18, D(2026, 7, 3)),
    ("Dropbox", "Business", "Monthly", "Hana Sato", 22, 16, D(2026, 7, 27)),
    ("Xero", "Standard (3 users)", "Monthly", "Ethan Nguyen", 20, 3, D(2026, 7, 10)),
    ("Cloud backup for Microsoft 365", "Per user", "Monthly", "Hana Sato", 4.50, 18, D(2026, 7, 14)),
    ("Endpoint protection", "Business (per device)", "Annual", "Hana Sato", 6, 20, D(2027, 4, 1)),
]
REPORT = D(2026, 7, 1)
CUR = [s[0] for s in STAFF if not s[4]]
LEFT = {s[0]: s[4] for s in STAFF if s[4]}


def licences():
    rnd = random.Random(7)
    recent = lambda: REPORT - dt.timedelta(days=rnd.randint(1, 45))
    rows = []
    def add(tool, people, when=None):
        for p in people:
            rows.append((tool, p, when(p) if when else (LEFT[p] - dt.timedelta(days=rnd.randint(0, 3)) if p in LEFT else recent())))
    add("Microsoft 365", CUR + list(LEFT))
    add("Adobe Creative Cloud", ["Leo Martin", "Priya Raman", "Tom Becker", "Aisha Khan", "Ben Walsh", "Sam Taylor", "Grace Liu",
                                 "Alex Romero", "Zoe Wright", "Marcus Lee"])
    rows.append(("Adobe Creative Cloud", "Maya Chen", REPORT - dt.timedelta(days=190)))
    add("Figma", ["Leo Martin", "Priya Raman", "Tom Becker", "Jordan Price", "Sam Taylor", "Grace Liu", "Ruby Ellis", "Zoe Wright", "Marcus Lee"])
    rows.append(("Figma", "Ben Walsh", REPORT - dt.timedelta(days=141)))
    add("Canva", ["Omar Haddad", "Ruby Ellis", "Chloe Dubois", "Hana Sato", "Alex Romero", "Grace Liu"])
    add("Zoom", ["Omar Haddad", "Ella Brooks"])
    for p, days in [("Maya Chen", 118), ("Hana Sato", 163), ("Chloe Dubois", 231)]:
        rows.append(("Zoom", p, REPORT - dt.timedelta(days=days)))
    add("Slack", CUR + list(LEFT))
    add("Dropbox", CUR + ["Ella Brooks"])
    add("Xero", ["Ethan Nguyen", "Hana Sato", "Maya Chen"])
    add("Cloud backup for Microsoft 365", CUR + list(LEFT))
    add("Endpoint protection", CUR)
    add("ChatGPT Plus (found on card)", ["Tom Becker", "Aisha Khan", "Omar Haddad"])
    add("Stock photos (found on card)", ["Priya Raman"])
    add("Grammarly (found on card)", ["Chloe Dubois", "Omar Haddad"])
    add("Zoom, second account (found on card)", ["Ruby Ellis"])
    return rows


def transactions():
    t = []
    months = [(2025 + (m > 12), (m - 1) % 12 + 1) for m in range(7, 19)]
    def monthly(day, desc, amount, cat, kind="Ongoing"):
        for y, m in months:
            t.append((D(y, m, day), desc, amount, cat, kind))
    sw, hw, net, sup, sec = CATS
    monthly(14, "MICROSOFT*365 BUS STD MSBILL.INFO", 378.00, sw)
    monthly(21, "ZOOM.COM 888-799-9666", 119.95, sw)
    monthly(9, "ZOOM.COM 888-799-9666", 23.99, sw)
    monthly(3, "SLACK T0123ABC DUBLIN", 243.00, sw)
    monthly(27, "DROPBOX*BUSINESS DUBLIN", 352.00, sw)
    monthly(10, "XERO AUSTRALIA PTY LTD", 60.00, sw)
    monthly(18, "STOCKIMG MONTHLY PLAN", 59.00, sw)
    for day in (5, 12, 24):
        monthly(day, "OPENAI *CHATGPT SUBSCR", 32.00, sw)
    monthly(14, "CLOUDSAFE BACKUP M365", 81.00, sec)
    monthly(2, "TELSTRA BUSINESS BILL", 399.00, net)
    monthly(1, "TECHCARE IT SERVICES", 990.00, sup)
    monthly(15, "PRINTWISE LEASING", 165.00, hw)
    t += [(D(2025, 8, 4), "ADOBE *CREATIVE CLD SYDNEY", 12958.56, sw, "Ongoing"),
          (D(2026, 2, 16), "FIGMA ANNUAL SAN FRANCISCO", 2880.00, sw, "Ongoing"),
          (D(2025, 11, 9), "CANVA* TEAMS ANNUAL SYDNEY", 2880.00, sw, "Ongoing"),
          (D(2026, 4, 1), "SECUREPOINT ENDPOINT ANNUAL", 1440.00, sec, "Ongoing"),
          (D(2025, 10, 14), "GRAMMARLY PREMIUM ANNUAL", 228.00, sw, "Ongoing"),
          (D(2026, 1, 20), "GRAMMARLY PREMIUM ANNUAL", 228.00, sw, "Ongoing"),
          (D(2026, 3, 2), "WEBNEST HOSTING+DOMAINS", 540.00, sw, "Ongoing"),
          (D(2026, 4, 16), "TECHCARE IT SERVICES REPAIR", 680.00, sup, "One-off"),
          (D(2025, 9, 23), "BIZTECH COMPUTERS MELBOURNE", 8697.00, hw, "One-off"),
          (D(2026, 2, 10), "DESKSUPPLY CO MONITORS+ACC", 1910.00, hw, "One-off")]
    rnd = random.Random(3)
    def other(day, desc, lo, hi, count=12, every=1):
        for i, (y, m) in enumerate(months):
            if i % every == 0 and count > 0:
                t.append((D(y, m, day), desc, round(rnd.uniform(lo, hi), 2) if lo != hi else lo, "Not IT", ""))
                count -= 1
    other(1, "COLLINS ST PROPERTY RENT", 5500.00, 5500.00)
    other(8, "BEAN THERE COFFEE SUPPLIES", 92, 168)
    other(11, "SPARKLE OFFICE CLEANING", 440.00, 440.00)
    other(28, "MONTHLY ACCOUNT FEE", 15.00, 15.00)
    other(19, "AGL ENERGY", 610, 890, 4, 3)
    other(22, "CITY WEST WATER", 120, 180, 4, 3)
    other(6, "OFFICE STATIONERY", 38, 145, 6, 2)
    other(16, "AUSTRALIA POST", 12, 64, 6, 2)
    other(25, "CITYSPRINT COURIERS", 28, 76, 4, 3)
    other(20, "STUDIO LUNCH CATERING", 180, 420, 5, 2)
    other(13, "CITY OF MELBOURNE RATES", 1240, 1240, 2, 6)
    other(4, "CLIENT GIFTS FLORIST", 85, 140, 2, 6)
    t += [(D(2025, 7, 30), "BIZCOVER INSURANCE ANNUAL", 2380.00, "Not IT", ""),
          (D(2025, 10, 31), "PARKER & CO ACCOUNTANTS", 3300.00, "Not IT", ""),
          (D(2026, 5, 29), "PARKER & CO ACCOUNTANTS", 1650.00, "Not IT", "")]
    t.sort(key=lambda r: (r[0], r[1]))
    return t


# ---------------------------------------------------------------- the sheets


def start_here(wb, example):
    ws = wb.active
    ws.title = "Start here"
    ws.column_dimensions["A"].width = 34
    ws.column_dimensions["B"].width = 16
    ws.column_dimensions["C"].width = 70
    put(ws, "A1", "Brightline Studio — IT costs 2025–26" if example else "IT cost templates", font=TITLE)
    put(ws, "A2", ("A worked example for the course IT on a Budget (Avro Academy). Brightline Studio and its prices are made up. "
                   "All amounts include GST.") if example else
        "Yellow cells are for your data. Everything else is a formula that fills itself in. All amounts include GST.", font=NOTE)
    put(ws, "A4", "Report date", font=BOLD)
    put(ws, "B4", REPORT if example else None, DATE, fill=YEL)
    put(ws, "C4", "warranty, age and “days since last used” are worked out from this date", font=NOTE)
    put(ws, "A5", "Replace laptops after (months)", font=BOLD)
    put(ws, "B5", 48, fill=YEL)
    put(ws, "C5", "used by the Assets sheet (Module 5)", font=NOTE)
    put(ws, "A6", "Current staff", font=BOLD)
    put(ws, "B6", '=COUNTIFS(Staff!A2:A1000,"<>",Staff!E2:E1000,"")')
    put(ws, "C6", "people in the Staff sheet with no leaving date", font=NOTE)
    rows = [("Sheet", "Module", "What it's for"),
            ("Transactions", "1", "a year of the bank statement and company cards, each line given a category"),
            ("Spend summary", "1", "IT spend by category, one-off vs ongoing, per person and the GST inside it"),
            ("Staff", "1, 3, 6", "who works here, and leaving dates"),
            ("Assets", "2, 5", "every device: warranty, age and when to replace it"),
            ("Subscriptions", "2, 3", "every tool you pay for: cost per year, seats in use and waste"),
            ("Licences", "3", "one row per seat from each tool's admin page: who has it and when they last used it"),
            ("Savings plan", "3", "each change and what it saves a year"),
            ("TCO", "4", "total cost of ownership of devices you're choosing between"),
            ("Budget", "5", "next year's IT budget, line by line")]
    for i, r in enumerate(rows):
        for j, v in enumerate(r):
            c = ws.cell(row=8 + i, column=1 + j, value=v)
            if i == 0:
                c.fill, c.font = NAVY, WHITE


def sheet_transactions(wb, example, data):
    ws = wb.create_sheet("Transactions")
    head(ws, ["Date", "Description (as on the statement)", "Amount (incl. GST)", "Category", "One-off or ongoing", "GST inside"],
         [12, 40, 16, 22, 17, 12])
    n = len(data) if example else 999
    for r in range(2, n + 2):
        if example:
            d, desc, amt, cat, kind = data[r - 2]
            put(ws, f"A{r}", d, DATE); put(ws, f"B{r}", desc); put(ws, f"C{r}", amt, MONEY)
            put(ws, f"D{r}", cat); put(ws, f"E{r}", kind or None)
        else:
            for col in "ABCDE":
                ws[f"{col}{r}"].fill = YEL
            ws[f"A{r}"].number_format = DATE; ws[f"C{r}"].number_format = MONEY
        put(ws, f"F{r}", f'=IF(OR(C{r}="",D{r}="Not IT"),"",ROUND(C{r}/11,2))', MONEY)
    last = n + 1
    dv = DataValidation(type="list", formula1='"' + ",".join(CATS + ["Not IT"]) + '"', allow_blank=True)
    dv2 = DataValidation(type="list", formula1='"One-off,Ongoing"', allow_blank=True)
    ws.add_data_validation(dv); ws.add_data_validation(dv2)
    dv.add(f"D2:D{last}"); dv2.add(f"E2:E{last}")
    ws.auto_filter.ref = f"A1:F{last}"
    return last


def sheet_summary(wb, last):
    ws = wb.create_sheet("Spend summary")
    head(ws, ["Category", "Spent", "Share"], [30, 16, 10])
    ws.freeze_panes = None
    rng = lambda col: f"Transactions!{col}$2:{col}${last}"
    for i, cat in enumerate(CATS, 2):
        put(ws, f"A{i}", cat)
        put(ws, f"B{i}", f"=SUMIFS({rng('C')},{rng('D')},A{i})", MONEY)
        put(ws, f"C{i}", f'=IF($B$7=0,"",B{i}/$B$7)', "0%")
    put(ws, "A7", "Total IT spend", font=BOLD); put(ws, "B7", "=SUM(B2:B6)", MONEY, BOLD, TOT); ws["A7"].fill = TOT
    put(ws, "A9", "One-off"); put(ws, "B9", f'=SUMIFS({rng("C")},{rng("E")},"One-off")', MONEY); put(ws, "C9", '=IF($B$7=0,"",B9/$B$7)', "0%")
    put(ws, "A10", "Ongoing"); put(ws, "B10", f'=SUMIFS({rng("C")},{rng("E")},"Ongoing")', MONEY); put(ws, "C10", '=IF($B$7=0,"",B10/$B$7)', "0%")
    put(ws, "A11", "Current staff"); put(ws, "B11", "='Start here'!B6")
    put(ws, "A12", "IT spend per person per year", font=BOLD); put(ws, "B12", '=IF(B11=0,"",B7/B11)', MONEY, BOLD)
    put(ws, "A13", "IT spend per person per month"); put(ws, "B13", '=IF(B11=0,"",B12/12)', MONEY)
    put(ws, "A14", "GST inside the total"); put(ws, "B14", "=ROUND(B7/11,2)", MONEY)
    put(ws, "A16", "One-off + ongoing should equal the total. If not, a line has a category but no One-off/Ongoing.", font=NOTE)


def sheet_staff(wb, example):
    ws = wb.create_sheet("Staff")
    head(ws, ["Name", "Role", "Started", "Laptop (asset tag)", "Left (leaving date)"], [20, 20, 12, 18, 18])
    rows = STAFF if example else [None] * 60
    for r, s in enumerate(rows, 2):
        for c, v in enumerate(s or (None,) * 5, 1):
            x = ws.cell(row=r, column=c, value=v)
            if c in (3, 5): x.number_format = DATE
            if not example: x.fill = YEL


def sheet_assets(wb, example):
    ws = wb.create_sheet("Assets")
    head(ws, ["Asset tag", "Type", "Assigned to", "Bought", "Price", "Warranty (years)", "Warranty ends", "Age (years)", "Warranty",
              "Replace by", "Due?"], [12, 10, 18, 11, 10, 10, 13, 9, 10, 12, 10])
    rows = ASSETS if example else [None] * 100
    for r, a in enumerate(rows, 2):
        for c, v in enumerate(a or (None,) * 6, 1):
            x = ws.cell(row=r, column=c, value=v)
            if c == 4: x.number_format = DATE
            if c == 5: x.number_format = MONEY0
            if not example: x.fill = YEL
        put(ws, f"G{r}", f'=IF(D{r}="","",EDATE(D{r},12*F{r}))', DATE)
        put(ws, f"H{r}", f"=IF(D{r}=\"\",\"\",ROUND(('Start here'!$B$4-D{r})/365.25,1))", "0.0")
        put(ws, f"I{r}", f"=IF(D{r}=\"\",\"\",IF(G{r}<'Start here'!$B$4,\"Expired\",\"Covered\"))")
        put(ws, f"J{r}", f"=IF(OR(D{r}=\"\",B{r}<>\"Laptop\"),\"\",EDATE(D{r},'Start here'!$B$5))", DATE)
        put(ws, f"K{r}", f"=IF(J{r}=\"\",\"\",IF(J{r}<'Start here'!$B$4,\"Overdue\",IF(J{r}<=EDATE('Start here'!$B$4,12),\"This year\",\"Later\")))")
    ws.auto_filter.ref = f"A1:K{len(rows) + 1}"
    dv = DataValidation(type="list", formula1='"Laptop,Desktop,Monitor,Phone,Tablet,Printer,Router,Other"', allow_blank=True)
    ws.add_data_validation(dv); dv.add(f"B2:B{len(rows) + 1}")


def sheet_subscriptions(wb, example, lic_last):
    ws = wb.create_sheet("Subscriptions")
    head(ws, ["Tool", "Plan", "Billing", "Owner", "Price per seat per month", "Seats paid for", "Seats in use", "Cost per year",
              "Seats not in use", "Wasted per year", "Renews"], [28, 24, 9, 14, 12, 9, 9, 13, 9, 13, 12])
    rows = SUBS if example else [None] * 30
    for r, s in enumerate(rows, 2):
        vals = s or (None,) * 7
        for c, v in zip([1, 2, 3, 4, 5, 6, 11], vals):
            x = ws.cell(row=r, column=c, value=v)
            if c == 5: x.number_format = MONEY
            if c == 11: x.number_format = DATE
            if not example: x.fill = YEL
        put(ws, f"G{r}", f'=IF(A{r}="","",COUNTIFS(Licences!$A$2:$A${lic_last},A{r},Licences!$E$2:$E${lic_last},"Active"))')
        put(ws, f"H{r}", f'=IF(A{r}="","",E{r}*F{r}*12)', MONEY)
        put(ws, f"I{r}", f'=IF(A{r}="","",MAX(0,F{r}-G{r}))')
        put(ws, f"J{r}", f'=IF(A{r}="","",I{r}*E{r}*12)', MONEY)
    t = len(rows) + 2
    put(ws, f"A{t}", "Total", font=BOLD)
    for col in "HJ":
        put(ws, f"{col}{t}", f"=SUM({col}2:{col}{t - 1})", MONEY, BOLD)
    for col in "ABCDEFGHIJK":
        ws[f"{col}{t}"].fill = TOT
    dv = DataValidation(type="list", formula1='"Monthly,Annual"', allow_blank=True)
    ws.add_data_validation(dv); dv.add(f"C2:C{t - 1}")
    return t


def sheet_licences(wb, example):
    ws = wb.create_sheet("Licences")
    head(ws, ["Tool", "Person", "Last used", "Days since last used", "Status"], [36, 18, 12, 12, 22])
    rows = licences() if example else [None] * 999
    for r, l in enumerate(rows, 2):
        for c, v in enumerate(l or (None,) * 3, 1):
            x = ws.cell(row=r, column=c, value=v)
            if c == 3: x.number_format = DATE
            if not example: x.fill = YEL
        put(ws, f"D{r}", f"=IF(C{r}=\"\",\"\",'Start here'!$B$4-C{r})", "0")
        put(ws, f"E{r}", f'=IF(B{r}="","",IF(COUNTIFS(Staff!$A$2:$A$1000,B{r},Staff!$E$2:$E$1000,"<>")>0,"Left the company",'
                         f'IF(D{r}>90,"Not used in 90+ days","Active")))')
    last = len(rows) + 1
    ws.auto_filter.ref = f"A1:E{last}"
    return last


def sheet_savings(wb, example):
    ws = wb.create_sheet("Savings plan")
    head(ws, ["Change", "Saves per year", "How it's worked out"], [46, 15, 60])
    if example:
        rows = [("Remove unused seats in every tool", "=SUM(Subscriptions!J2:J11)", "Subscriptions: wasted per year, all tools"),
                ("Cancel Zoom (use Teams)", "=Subscriptions!H6-Subscriptions!J6", "the rest of Zoom — its unused seats are already in row 2"),
                ("Cancel the second Zoom account", "=23.99*12", "found on a company card (Module 2)"),
                ("Move from Dropbox to OneDrive/SharePoint, then cancel", "=Subscriptions!H8-Subscriptions!J8",
                 "the rest of Dropbox — its unused seats are already in row 2")]
        for r, (a, b, c) in enumerate(rows, 2):
            put(ws, f"A{r}", a); put(ws, f"B{r}", b, MONEY); put(ws, f"C{r}", c, font=NOTE)
        put(ws, "A6", "Total savings per year", font=BOLD); put(ws, "B6", "=SUM(B2:B5)", MONEY, BOLD)
        put(ws, "A7", "Share of the subscription bill"); put(ws, "B7", "=B6/Subscriptions!H12", "0%")
    else:
        for r in range(2, 12):
            ws[f"A{r}"].fill = YEL; ws[f"B{r}"].fill = YEL; ws[f"C{r}"].fill = YEL; ws[f"B{r}"].number_format = MONEY
        put(ws, "A12", "Total savings per year", font=BOLD); put(ws, "B12", "=SUM(B2:B11)", MONEY, BOLD)
        put(ws, "A14", "Tip: link to the other sheets (like =SUM(Subscriptions!J2:J31)) so the plan updates itself, and never count "
                       "a saving twice.", font=NOTE)
    for col in "ABC":
        ws[f"{col}{6 if example else 12}"].fill = TOT


def sheet_tco(wb, example):
    ws = wb.create_sheet("TCO")
    head(ws, ["Option", "Price", "Extra warranty", "Setup", "Repairs and support per year", "Years in use", "Resale at the end",
              "Monthly fee", "Total cost of ownership", "Cost per year"], [24, 10, 10, 9, 13, 9, 10, 10, 14, 12])
    rows = [("A: Budget laptop", 1899, 249, 150, 250, 3, 200, 0), ("B: Design laptop", 2899, 0, 150, 80, 4, 400, 0),
            ("C: Lease", 0, 0, 0, 0, 3, 0, 79)] if example else [None] * 6
    for r, o in enumerate(rows, 2):
        for c, v in enumerate(o or (None,) * 8, 1):
            x = ws.cell(row=r, column=c, value=v)
            if c in (2, 3, 4, 5, 7, 8): x.number_format = MONEY0
            if not example: x.fill = YEL
        put(ws, f"I{r}", f'=IF(A{r}="","",B{r}+C{r}+D{r}+E{r}*F{r}+H{r}*12*F{r}-G{r})', MONEY)
        put(ws, f"J{r}", f'=IF(A{r}="","",I{r}/F{r})', MONEY)
    put(ws, f"A{len(rows) + 3}", "Costs you can't see here: lost time on a slow device, downtime during repairs, staff happiness.", font=NOTE)


def sheet_budget(wb, example):
    ws = wb.create_sheet("Budget")
    head(ws, ["Line", "Next year (2026–27)", "Notes: how it was worked out"], [34, 16, 80])
    if example:
        rows = [("Software subscriptions",
                 "=Subscriptions!H12-Subscriptions!H10-Subscriptions!H11-('Savings plan'!B6-Subscriptions!J10-Subscriptions!J11)",
                 "the register's yearly cost, minus the savings plan (backup and security are their own line)"),
                ("Tools found on cards", "=(32*3+59+19*2)*12",
                 "ChatGPT ×3, stock photos and Grammarly ×2: kept, now approved and tracked (second Zoom cancelled)"),
                ("Domain names and hosting", 540, "yearly"),
                ("Laptop replacements", "=5*TCO!B3", "5 × $2,899 (option B) — the five overdue staff laptops"),
                ("Printer lease", "=165*12", "$165 × 12"),
                ("Internet and mobiles", "=(129+6*45)*12", "(NBN $129 + 6 phones × $45) × 12"),
                ("IT support", "=990*12+1000", "$990 × 12, plus $1,000 for repairs and call-outs"),
                ("Backup and endpoint protection", "=Subscriptions!H10+Subscriptions!H11-Subscriptions!J10-Subscriptions!J11",
                 "kept — just without the unused seats"),
                ("Contingency (10%)", "=ROUND(SUM(B2:B9)*0.1,0)", "for surprises: a stolen laptop, a price rise")]
        for r, (a, b, c) in enumerate(rows, 2):
            put(ws, f"A{r}", a); put(ws, f"B{r}", b, MONEY); put(ws, f"C{r}", c, font=NOTE)
        put(ws, "A11", "Total", font=BOLD); put(ws, "B11", "=SUM(B2:B10)", MONEY, BOLD)
        put(ws, "A13", "Last year's actual IT spend"); put(ws, "B13", "='Spend summary'!B7", MONEY)
        put(ws, "A14", "Difference (next year − last year)"); put(ws, "B14", "=B11-B13", MONEY)
        for col in "ABC": ws[f"{col}11"].fill = TOT
    else:
        lines = ["Software subscriptions", "Hardware (new and replacement devices)", "Leases", "Internet and phones",
                 "IT support", "Security and backup", "", "", ""]
        for r, a in enumerate(lines, 2):
            put(ws, f"A{r}", a or None, fill=YEL); ws[f"B{r}"].fill = YEL; ws[f"C{r}"].fill = YEL; ws[f"B{r}"].number_format = MONEY
        put(ws, "A11", "Contingency rate"); put(ws, "B11", 0.1, "0%", fill=YEL)
        put(ws, "A12", "Contingency"); put(ws, "B12", "=ROUND(SUM(B2:B10)*B11,0)", MONEY)
        put(ws, "A13", "Total", font=BOLD); put(ws, "B13", "=SUM(B2:B10)+B12", MONEY, BOLD)
        put(ws, "A15", "Last year's actual IT spend"); put(ws, "B15", "='Spend summary'!B7", MONEY)
        put(ws, "A16", "Difference (next year − last year)"); put(ws, "B16", "=B13-B15", MONEY)
        for col in "ABC": ws[f"{col}13"].fill = TOT


def build(example):
    wb = Workbook()
    data = transactions() if example else None
    start_here(wb, example)
    last = sheet_transactions(wb, example, data)
    sheet_summary(wb, last)
    sheet_staff(wb, example)
    sheet_assets(wb, example)
    t = sheet_subscriptions(wb, example, 128 if example else 1000)
    lic_last = sheet_licences(wb, example)
    assert not example or lic_last == 128, lic_last
    sheet_savings(wb, example)
    sheet_tco(wb, example)
    sheet_budget(wb, example)
    for ws in wb.worksheets:
        ws.sheet_view.zoomScale = 110
    wb.calculation.fullCalcOnLoad = True  # Excel and Google Sheets work out every formula when the file opens
    name = "Brightline-IT-Costs.xlsx" if example else "IT-Cost-Templates.xlsx"
    os.makedirs(BUILD, exist_ok=True)
    wb.save(os.path.join(BUILD, name))
    if example:
        print("transactions", len(data), "IT lines", sum(1 for r in data if r[3] != "Not IT"), "licence rows", lic_last - 1)


if __name__ == "__main__":
    build(True)
    build(False)
