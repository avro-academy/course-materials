"""Builds Spreadsheet-Practice-Workbook.xlsx into ../build."""
import os
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'build', 'Spreadsheet-Practice-Workbook.xlsx')
NAVY = PatternFill('solid', fgColor='1D2B4F'); YEL = PatternFill('solid', fgColor='FFF6D6'); W = Font(color='FFFFFF', bold=True)
I = Font(italic=True, color='56607A')

def head(ws, row, cols, widths):
    for i, (c, w) in enumerate(zip(cols, widths), 1):
        x = ws.cell(row=row, column=i, value=c); x.fill = NAVY; x.font = W; x.alignment = Alignment(wrap_text=True, vertical='center')
        ws.column_dimensions[x.column_letter].width = w

wb = Workbook()
# 1 Hours and pay
ws = wb.active; ws.title = '1 Hours and pay'
ws['A1'] = 'Task: work out the pay for each shift (Hours × Rate) in column D, then the totals in row 10.'; ws['A1'].font = I
ws['A2'] = 'Yellow cells are for you. Use =B4*C4 in D4 and fill it down; use =SUM() for the totals. Check on the Answers sheet.'; ws['A2'].font = I
head(ws, 3, ['Day', 'Hours', 'Rate ($/hr)', 'Pay ($)'], [14, 10, 12, 12])
shifts = [('Monday', 4, 26.50), ('Tuesday', 0, 26.50), ('Wednesday', 5, 26.50), ('Thursday', 3.5, 26.50), ('Friday', 6, 26.50), ('Saturday', 7, 33.15)]
for r, (d, h, rate) in enumerate(shifts, 4):
    ws.cell(row=r, column=1, value=d); ws.cell(row=r, column=2, value=h); ws.cell(row=r, column=3, value=rate).number_format = '0.00'
    ws.cell(row=r, column=4).fill = YEL
ws['A10'] = 'Total'; ws['A10'].font = Font(bold=True)
for c in ('B10', 'D10'): ws[c].fill = YEL
ws['A12'] = 'Bonus: in B12, use =AVERAGE() to find the average hours per day, and in B13 use =MAX() to find the longest shift.'; ws['A12'].font = I
ws['B12'].fill = YEL; ws['B13'].fill = YEL
# 2 Stock list
ws = wb.create_sheet('2 Stock list')
ws['A1'] = 'Task: sort by Quantity (smallest first), then filter Reorder? to show only "Yes". In D2 use =COUNTIF(E5:E20,"Yes") to count items to reorder.'; ws['A1'].font = I
ws['A2'] = 'Items to reorder:'; ws['A2'].font = Font(bold=True); ws['D2'].fill = YEL
head(ws, 4, ['Item', 'Category', 'Quantity', 'Reorder level', 'Reorder?'], [26, 14, 10, 13, 10])
stock = [('Takeaway cups 8oz', 'Packaging', 120, 100), ('Takeaway cups 12oz', 'Packaging', 40, 100), ('Lids', 'Packaging', 300, 150),
         ('Napkins (pack)', 'Packaging', 3, 5), ('Paper bags', 'Packaging', 60, 50), ('Full cream milk (L)', 'Dairy', 8, 12),
         ('Oat milk (L)', 'Dairy', 2, 6), ('Soy milk (L)', 'Dairy', 7, 6), ('Coffee beans (kg)', 'Coffee', 4, 5),
         ('Decaf beans (kg)', 'Coffee', 2, 1), ('Chai powder (kg)', 'Tea', 1, 1), ('English breakfast tea (box)', 'Tea', 6, 2),
         ('Banana bread (loaf)', 'Food', 1, 3), ('Muffins', 'Food', 14, 10), ('Sugar sachets (box)', 'Other', 2, 2), ('Hand towels (pack)', 'Cleaning', 9, 4)]
for r, (a, b, q, lvl) in enumerate(stock, 5):
    for c, v in enumerate((a, b, q, lvl, 'Yes' if q < lvl else 'No'), 1): ws.cell(row=r, column=c, value=v)
ws.auto_filter.ref = 'A4:E20'; ws.freeze_panes = 'A5'
ws['G4'] = 'Reorder? says Yes when Quantity is less than Reorder level.'; ws['G4'].font = I
# 3 Weekly sales
ws = wb.create_sheet('3 Weekly sales')
ws['A1'] = 'Task: total each day in column F and each column in row 12. Then select A3:A10 and F3:F10 and insert a column chart. Which day was busiest?'; ws['A1'].font = I
head(ws, 3, ['Day', 'Coffee', 'Tea', 'Food', 'Other', 'Total ($)'], [14, 11, 11, 11, 11, 12])
sales = [('Monday', 412, 64, 318, 22), ('Tuesday', 388, 58, 296, 18), ('Wednesday', 455, 71, 344, 25), ('Thursday', 470, 66, 362, 30),
         ('Friday', 598, 80, 471, 41), ('Saturday', 812, 104, 690, 66), ('Sunday', 705, 97, 612, 52)]
for r, row in enumerate(sales, 4):
    for c, v in enumerate(row, 1): ws.cell(row=r, column=c, value=v)
    ws.cell(row=r, column=6).fill = YEL
ws['A12'] = 'Total'; ws['A12'].font = Font(bold=True)
for c in 'BCDEF': ws[f'{c}12'].fill = YEL
ws['A14'] = 'Busiest day:'; ws['B14'].fill = YEL; ws['A15'] = 'Average daily total:'; ws['B15'].fill = YEL
ws['D14'] = 'Hint: =MAX(F4:F10) finds the biggest total; =AVERAGE(F4:F10) the average.'; ws['D14'].font = I
# Answers
a = wb.create_sheet('Answers')
a['A1'] = 'Answers (try the sheets first!)'; a['A1'].font = Font(size=14, bold=True, color='1D2B4F')
a['A3'] = '1 Hours and pay'; a['A3'].font = Font(bold=True)
head(a, 4, ['Day', 'Hours', 'Rate ($/hr)', 'Pay ($)', 'Formula in Pay'], [26, 14, 12, 12, 26])
for r, (d, h, rate) in enumerate(shifts, 5):
    a.cell(row=r, column=1, value=d); a.cell(row=r, column=2, value=h); a.cell(row=r, column=3, value=rate)
    a.cell(row=r, column=4, value=f'=B{r}*C{r}').number_format = '0.00'; a.cell(row=r, column=5, value=f'Type =B{r-1}*C{r-1} on sheet 1')
a['A11'] = 'Total'; a['B11'] = '=SUM(B5:B10)'; a['D11'] = '=SUM(D5:D10)'; a['D11'].number_format = '0.00'; a['E11'] = 'Type =SUM(B4:B9) and =SUM(D4:D9)'
a['A12'] = 'Average hours'; a['B12'] = '=AVERAGE(B5:B10)'; a['B12'].number_format = '0.00'
a['A13'] = 'Longest shift'; a['B13'] = '=MAX(B5:B10)'
a['A15'] = '2 Stock list'; a['A15'].font = Font(bold=True)
low = sorted([s for s in stock if s[2] < s[3]], key=lambda s: s[2])
a['A16'] = f'Items to reorder: {len(low)}  (=COUNTIF(E5:E20,"Yes"))'
for i, s in enumerate(low, 17): a.cell(row=i, column=1, value=s[0]); a.cell(row=i, column=2, value=f'{s[2]} (reorder at {s[3]})')
r0 = 17 + len(low) + 1
a.cell(row=r0, column=1, value='3 Weekly sales').font = Font(bold=True)
head(a, r0 + 1, ['Day', 'Total ($)'], [26, 14])
for i, row in enumerate(sales, r0 + 2):
    a.cell(row=i, column=1, value=row[0]); a.cell(row=i, column=2, value=sum(row[1:]))
tot = sum(sum(s[1:]) for s in sales)
a.cell(row=r0 + 9, column=1, value='Week total'); a.cell(row=r0 + 9, column=2, value=tot)
a.cell(row=r0 + 10, column=1, value='Busiest day'); a.cell(row=r0 + 10, column=2, value='Saturday ($1,672)')
a.cell(row=r0 + 11, column=1, value='Average daily total'); a.cell(row=r0 + 11, column=2, value=round(tot / 7, 2))
wb.save(OUT); print('workbook ok')
