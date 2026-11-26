"""Builds QA-Templates.xlsx and Test-Plan-Template.docx into ../build."""
import os
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from docx import Document
from docx.shared import Pt, RGBColor

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'build')
navy = PatternFill('solid', fgColor='1D2B4F')
white = Font(color='FFFFFF', bold=True)
thin = Side(style='thin', color='D0D6E2')


def sheet(ws, title, headers, widths, example=None, rows=40, validations=()):
    ws.title = title
    ws.append(headers)
    for i, w in enumerate(widths, 1):
        c = ws.cell(row=1, column=i)
        c.fill = navy
        c.font = white
        c.alignment = Alignment(wrap_text=True, vertical='center')
        ws.column_dimensions[c.column_letter].width = w
    ws.row_dimensions[1].height = 30
    if example:
        ws.append(example)
        for c in ws[2]:
            c.font = Font(italic=True, color='56607A')
    for r in range(2, rows + 2):
        for col in range(1, len(headers) + 1):
            cell = ws.cell(row=r, column=col)
            cell.alignment = Alignment(wrap_text=True, vertical='top')
            cell.border = Border(bottom=thin)
    for col, opts in validations:
        dv = DataValidation(type='list', formula1='"' + ','.join(opts) + '"', allow_blank=True)
        ws.add_data_validation(dv)
        dv.add(f'{col}2:{col}{rows + 1}')
    ws.freeze_panes = 'A2'


wb = Workbook()
sheet(wb.active, 'Test cases',
      ['ID', 'Requirement', 'Title', 'Preconditions', 'Steps', 'Test data', 'Expected result', 'Actual result', 'Status', 'Bug ID'],
      [8, 12, 32, 24, 40, 18, 32, 28, 10, 10],
      ['TC-08', 'REQ-8', 'Discount code STUDENT10 takes 10% off', 'App open; nothing in the order',
       '1. Add Ham and cheese toastie ($9.50)\n2. Type STUDENT10 in Discount code\n3. Click Apply', 'Code: STUDENT10',
       'Discount −$0.95, total $8.55, message "STUDENT10 applied: 10% off."', '', '', ''],
      validations=[('I', ['Pass', 'Fail', 'Blocked', 'Not run'])])
sheet(wb.create_sheet(), 'Bug log',
      ['Bug ID', 'Title', 'Requirement', 'Steps to reproduce', 'Expected', 'Actual', 'Severity', 'Priority', 'Environment', 'Status', 'Evidence'],
      [8, 34, 12, 40, 26, 26, 11, 10, 22, 12, 16],
      ['BUG-01', 'Names with an apostrophe are refused at checkout', 'REQ-11',
       "1. Add Banana bread\n2. Go to checkout\n3. Name: Sam O'Brien, mobile 0412345678\n4. Place order",
       'The order is placed', '"Enter your name (2 to 40 letters)."', 'Major', 'High', 'Windows 11, Chrome, 1280 × 800', 'New', 'screenshot-01.png'],
      validations=[('G', ['Critical', 'Major', 'Minor', 'Trivial']), ('H', ['High', 'Medium', 'Low']),
                   ('J', ['New', 'Open', 'Fixed', 'Retest', 'Closed', 'Reopened', "Won't fix", 'Duplicate'])])
ws = wb.create_sheet()
sheet(ws, 'Exploratory session', ['Time', 'What I tried', 'What happened', 'Bug? / Question'], [12, 45, 45, 30],
      ['10:00', 'Read every item and price', 'All 12 items show. Several prices look odd', 'Possible bug (REQ-1)'])
ws.insert_rows(1, 4)
for r, (k, v) in enumerate([('Charter', 'Explore … with … to discover …'), ('Tester', ''),
                            ('Time box', 'e.g. 30 minutes'), ('Environment', 'Browser, device, window size')], 1):
    ws.cell(row=r, column=1, value=k).font = Font(bold=True)
    ws.cell(row=r, column=2, value=v).font = Font(italic=True, color='56607A')
ws.freeze_panes = 'A6'
wb.save(os.path.join(out, 'QA-Templates.xlsx'))

d = Document()
d.styles['Normal'].font.name = 'Calibri'
d.styles['Normal'].font.size = Pt(11)
d.add_heading('Test plan: Order Ahead 1.0', 0)
d.add_paragraph('Fill in each section. A page or two is plenty for a small project. The grey text is an example from the course: replace it with your own.')


def section(title, hint):
    d.add_heading(title, 1)
    p = d.add_paragraph(hint)
    p.runs[0].font.color.rgb = RGBColor(0x6B, 0x75, 0x90)
    p.runs[0].italic = True


section('1. About this plan', 'Project, version, who wrote the plan, date.')
section('2. In scope', 'Menu, search, options, Your order, discount code, checkout, confirmation (REQ-1 to REQ-18).')
section('3. Out of scope', "Payment (done at the counter); the café's kitchen screens.")
section('4. Approach', 'Test cases from the requirements; boundary and decision-table tests; three exploratory sessions; phone and keyboard checks; a few automated tests.')
section('5. Environments', 'Windows + Chrome and Edge; Android + Chrome; iPhone + Safari; 375 px and 1280 px.')
d.add_heading('6. Risks', 1)
t = d.add_table(rows=1, cols=4)
t.style = 'Light Grid Accent 1'
for i, x in enumerate(['Area', 'Likely to break?', 'Impact if it does', 'Risk']):
    t.rows[0].cells[i].text = x
for row in [('Totals and discounts', 'Medium — lots of calculations', 'High — customers charged wrongly', 'High'),
            ('Checkout form', 'Medium — lots of rules', 'High — no order at all', 'High'),
            ('Phone layout', 'Medium', 'High — most customers use phones', 'High'),
            ('Category filter', 'Low', 'Low — search and All still work', 'Low'), ('', '', '', ''), ('', '', '', '')]:
    cells = t.add_row().cells
    for i, x in enumerate(row):
        cells[i].text = x
section('7. Entry criteria', 'Requirements agreed; the app builds and opens.')
section('8. Exit criteria', 'All planned tests run; no open Critical or Major bugs; Minor bugs agreed with the café.')
section('9. Schedule and people', 'Who tests what, and when.')
section('10. Deliverables', 'Test cases, bug log, exploratory session notes, test summary report.')
d.save(os.path.join(out, 'Test-Plan-Template.docx'))
print('templates ok')
