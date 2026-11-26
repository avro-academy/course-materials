"""Builds the Word templates and the Excel tracker for Job Ready into ../build."""
import os, datetime
from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import FormulaRule

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'build')
GREY = RGBColor(0x80, 0x80, 0x80); NAVY = RGBColor(0x1D, 0x2B, 0x4F); TEAL = RGBColor(0x2B, 0xB3, 0xA3)


def base(font='Calibri'):
    d = Document()
    for s in d.sections:
        s.left_margin = s.right_margin = Cm(2); s.top_margin = s.bottom_margin = Cm(1.6)
    st = d.styles['Normal']; st.font.name = font; st.font.size = Pt(11)
    st.element.rPr.rFonts.set(qn('w:eastAsia'), font)
    st.paragraph_format.space_after = Pt(3)
    return d


def note(d, text):
    p = d.add_paragraph(); r = p.add_run('Note: ' + text); r.italic = True; r.font.size = Pt(9); r.font.color.rgb = GREY
    return p


def rule_below(p, color='1D2B4F'):
    pPr = p._p.get_or_add_pPr(); b = OxmlElement('w:pBdr'); bt = OxmlElement('w:bottom')
    for k, v in (('val', 'single'), ('sz', '8'), ('space', '1'), ('color', color)): bt.set(qn('w:' + k), v)
    b.append(bt); pPr.append(b)


SECTIONS = [
    ('Career objective', ['[2–3 sentences: who you are, the job you want, and your availability.]'],
     'Example: "Motivated and reliable TAFE student looking for a casual kitchen hand role. Experienced in fast-paced canteen work and comfortable following food safety rules. Available weekends and weekday evenings."'),
    ('Key skills', ['[Skill] — [a short example that proves it]', '[Skill] — [example]', '[Skill] — [example]', '[Skill] — [example]'],
     '4–6 skills that match the job ad, each with proof. Use the Action verbs and skills word bank.'),
    ('Experience', None, 'Jobs, volunteering, work experience, sport or club roles. Most recent first. 2–4 bullet points each: action verb + what you did + result or detail.'),
    ('Education', ['[School, TAFE or uni] — [year level or qualification], [year]', '[Relevant subjects or achievements]'], None),
    ('Certificates and licences', ['[e.g. First aid (HLTAID011), 2025]', '[e.g. Food safety certificate, 2025]'],
     'First aid, RSA, White Card, food safety, driver licence, online courses. Delete this section if you have none yet.'),
    ('Achievements and interests', ['[Awards, sport, leadership, hobbies: short and positive]'], None),
    ('Referees', ['[Name], [Role], [Organisation] — [phone] · [email]', '[Name], [Role], [Organisation] — [phone] · [email]'],
     'Two people who can vouch for you, not family or friends. Ask them first. Or write "Available on request".'),
]
EXP = [('[Role], [Organisation] — [Month Year] – [Month Year or Present]',
        ['[Action verb + what you did + result or detail]', '[Action verb + what you did + result or detail]', '[Action verb + what you did + result or detail]'])] * 2


def resume(modern):
    d = base('Calibri' if not modern else 'Arial')
    note(d, 'The grey notes explain what to write. Replace everything in [square brackets], then delete every note. '
            'Keep it to one page and save it as a PDF named Firstname-Lastname-Resume.pdf.')
    p = d.add_paragraph(); r = p.add_run('[YOUR FULL NAME]' if modern else '[Your Full Name]'); r.bold = True
    r.font.size = Pt(24 if modern else 20)
    if modern: r.font.color.rgb = NAVY
    p.paragraph_format.space_after = Pt(0)
    p = d.add_paragraph('[Suburb, State] · [Mobile] · [firstname.lastname@email.com] · [Available: days and times]')
    p.runs[0].font.size = Pt(10)
    if modern: p.runs[0].font.color.rgb = TEAL; rule_below(p, '2BB3A3')
    note(d, 'Phone and email at the top. Use a professional email. No photo, age, religion or full street address.')
    for title, lines, hint in SECTIONS:
        h = d.add_paragraph(); hr = h.add_run(title.upper() if modern else title); hr.bold = True
        hr.font.size = Pt(12 if modern else 13)
        if modern: hr.font.color.rgb = NAVY; hr.font.all_caps = True
        else: rule_below(h, '999999')
        h.paragraph_format.space_before = Pt(10)
        if hint: note(d, hint)
        if title == 'Experience':
            for role, bullets in EXP:
                rp = d.add_paragraph(); rr = rp.add_run(role); rr.bold = True
                for b in bullets: d.add_paragraph(b, style='List Bullet')
        else:
            for ln in lines:
                d.add_paragraph(ln, style='List Bullet' if title in ('Key skills', 'Achievements and interests') else None)
    d.save(os.path.join(OUT, 'Resume-Template-Modern.docx' if modern else 'Resume-Template-Plain.docx'))


def cover_letter():
    d = base()
    note(d, 'Replace everything in [square brackets] and delete these notes. Keep it under one page (about 250–350 words) '
            'and change it for every job. If you apply by email, you can paste the letter into the email body and attach your resume.')
    for ln in ['[Your full name]', '[Suburb, State] · [Mobile] · [Professional email]', '', '[Date]', '',
               '[Manager\'s name, if you can find it]', '[Business name]', '[Business suburb, State]', '']:
        d.add_paragraph(ln)
    d.add_paragraph('Dear [Manager\'s name / Hiring Manager],')
    note(d, 'Paragraph 1, why you\'re writing: the job, where you saw it, and one sentence on why you\'re a great fit.')
    d.add_paragraph('I\'m writing to apply for the [job title] position advertised on [where you saw it]. As a [two or three words that describe you] '
                    '[student / person] who [something relevant you enjoy or do well], I\'d be a great fit for your team.')
    note(d, 'Paragraph 2, why you: pick 2–3 things from the job ad and back each one up with an example. Use the ad\'s own words.')
    d.add_paragraph('[For the past … I\'ve … — an example that shows the first thing they asked for.] [Another example that shows the second thing.] '
                    '[A certificate, skill or your availability that matches the ad.]')
    note(d, 'Paragraph 3, why them and the next step: something you like about the business, your availability, and a thank you.')
    d.add_paragraph('[Something genuine you like about the business.] I\'d love the chance to be part of your team. I\'m available [days and times]. '
                    'My resume is attached, and I can be contacted on [mobile] or [email]. Thank you for considering my application.')
    d.add_paragraph('Kind regards,'); d.add_paragraph('[Your full name]')
    d.add_paragraph()
    h = d.add_paragraph(); h.add_run('Before you send it').bold = True
    for c in ['The job title and business name are right', 'It mentions 2–3 things from the ad, with examples', 'Your availability is included',
              'Spellcheck, then read it out loud', 'All the notes and [brackets] are gone', 'Saved as Firstname-Lastname-Cover-Letter.pdf (unless it\'s in the email body)']:
        d.add_paragraph('☐ ' + c)
    d.save(os.path.join(OUT, 'Cover-Letter-Template.docx'))


def tracker():
    wb = Workbook(); ws = wb.active; ws.title = 'Applications'
    navy = PatternFill('solid', fgColor='1D2B4F'); thin = Side(style='thin', color='D0D6E2')
    heads = ['Date applied', 'Business', 'Job title', 'Where I found it', 'Contact name / link', 'Resume tailored?', 'Cover letter sent?',
             'Status', 'Follow-up date', 'Interview date', 'Notes']
    widths = [13, 22, 22, 16, 26, 11, 11, 15, 13, 13, 40]
    ws.append(heads)
    for i, w in enumerate(widths, 1):
        c = ws.cell(row=1, column=i); c.fill = navy; c.font = Font(color='FFFFFF', bold=True)
        c.alignment = Alignment(wrap_text=True, vertical='center'); ws.column_dimensions[c.column_letter].width = w
    ws.row_dimensions[1].height = 32
    ws.append([datetime.date(2026,3,10), 'Example: Corner Café', 'Casual Café Crew', 'SEEK', 'Mel Carter', 'Yes', 'Yes', 'Followed up',
               datetime.date(2026,3,17), '', 'Delete this example row. Called on 17/3 — manager said interviews next week.'])
    N = 200
    for r in range(2, N + 2):
        for col in range(1, len(heads) + 1):
            c = ws.cell(row=r, column=col); c.border = Border(bottom=thin); c.alignment = Alignment(vertical='top', wrap_text=col == 11)
        for col in (1, 9, 10): ws.cell(row=r, column=col).number_format = 'DD/MM/YYYY'
    for c in ws[2]: c.font = Font(italic=True, color='56607A')
    yn = DataValidation(type='list', formula1='"Yes,No"', allow_blank=True); ws.add_data_validation(yn); yn.add(f'F2:G{N+1}')
    stv = DataValidation(type='list', formula1='"Applied,Followed up,Interview,Offer,Unsuccessful"', allow_blank=True)
    ws.add_data_validation(stv); stv.add(f'H2:H{N+1}')
    rng = f'A2:K{N+1}'
    ws.conditional_formatting.add(rng, FormulaRule(formula=['$H2="Interview"'], fill=PatternFill('solid', fgColor='FFF1C9')))
    ws.conditional_formatting.add(rng, FormulaRule(formula=['$H2="Offer"'], fill=PatternFill('solid', fgColor='D3F2EC')))
    ws.conditional_formatting.add(rng, FormulaRule(formula=['$H2="Unsuccessful"'], font=Font(color='9AA3B5')))
    ws.conditional_formatting.add(f'I2:I{N+1}', FormulaRule(formula=['AND($I2<>"",$I2<=TODAY(),$H2="Applied")'], fill=PatternFill('solid', fgColor='FFD9DA')))
    ws.freeze_panes = 'A2'; ws.auto_filter.ref = f'A1:K{N+1}'
    s = wb.create_sheet('Summary')
    s['A1'] = 'My job search summary'; s['A1'].font = Font(size=16, bold=True, color='1D2B4F')
    s['A2'] = 'This tab counts automatically from the Applications tab.'; s['A2'].font = Font(italic=True, color='56607A')
    rows = [('Applications sent', '=COUNTA(Applications!B2:B201)'),
            ('Waiting to hear back', '=COUNTIF(Applications!H2:H201,"Applied")+COUNTIF(Applications!H2:H201,"Followed up")'),
            ('Interviews', '=COUNTIF(Applications!H2:H201,"Interview")'),
            ('Offers', '=COUNTIF(Applications!H2:H201,"Offer")'),
            ('Unsuccessful', '=COUNTIF(Applications!H2:H201,"Unsuccessful")'),
            ('Tailored resume', '=COUNTIF(Applications!F2:F201,"Yes")'),
            ('Cover letters sent', '=COUNTIF(Applications!G2:G201,"Yes")'),
            ('Follow-ups due (date passed, status still Applied)', '=COUNTIFS(Applications!I2:I201,"<="&TODAY(),Applications!H2:H201,"Applied")')]
    for i, (k, f) in enumerate(rows, 4):
        s.cell(row=i, column=1, value=k).font = Font(bold=True); c = s.cell(row=i, column=2, value=f); c.font = Font(size=13, color='1D2B4F')
    s.column_dimensions['A'].width = 48; s.column_dimensions['B'].width = 12
    s['A14'] = 'Tip: follow up about a week after applying, then change the status to "Followed up".'; s['A14'].font = Font(italic=True, color='56607A')
    wb.save(os.path.join(OUT, 'Job-Application-Tracker.xlsx'))


resume(False); resume(True); cover_letter(); tracker(); print('office files built')
