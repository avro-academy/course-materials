"""Builds Prompt-Library-Template.docx into ../build."""
import os
from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'build', 'Prompt-Library-Template.docx')
NAVY, CORAL, GREY = RGBColor(0x1D, 0x2B, 0x4F), RGBColor(0xFF, 0x5A, 0x5F), RGBColor(0x6B, 0x75, 0x90)

d = Document()
for s in d.sections:
    s.left_margin = s.right_margin = Cm(2); s.top_margin = s.bottom_margin = Cm(1.8)
d.styles['Normal'].font.name = 'Calibri'; d.styles['Normal'].font.size = Pt(11)
for st in ('Title', 'Heading 1', 'Heading 2'):
    d.styles[st].font.color.rgb = NAVY; d.styles[st].font.name = 'Calibri'


def shade(cell, hex_):
    tc = cell._tc.get_or_add_tcPr(); sh = OxmlElement('w:shd')
    sh.set(qn('w:val'), 'clear'); sh.set(qn('w:color'), 'auto'); sh.set(qn('w:fill'), hex_); tc.append(sh)


def hint(text, p=None):
    p = p or d.add_paragraph(); r = p.add_run(text); r.italic = True; r.font.color.rgb = GREY; return p


d.add_heading('My prompt library', 0)
p = d.add_paragraph(); r = p.add_run('Prompt Right: Get Great Results from Free AI Tools · Avro Academy'); r.font.color.rgb = CORAL; r.bold = True
d.add_paragraph('Name: ______________________________    Started: ____ / ____ / ________')
d.add_paragraph('Keep the prompts that work. Put [square brackets] around the parts that change each time, '
                'test every prompt on a real situation, and improve it at least once. Never put private information '
                '(addresses, phone numbers, passwords, other people\'s details) in a saved prompt.')

d.add_heading('Your task', 1)
for t in ['Choose 5 tasks you really do (or will do): at least one for work or job hunting, one for study and one for everyday life.',
          'Write a reusable prompt for each, using the 4 parts (task, context, format, audience), examples, limits and "ask me first".',
          'Test each one on a real situation and improve it at least once.',
          'Add a checking step to each: what must you verify before you use the answer?']:
    d.add_paragraph(t, style='List Number')

FIELDS = ['What it\'s for', 'Area', 'The prompt', 'Which tool worked best', 'Follow-up that improves it', 'What I check before using it', 'Tested on', 'What I changed after testing']


def card(n, vals=None):
    d.add_heading(f'Prompt {n}' if not vals else 'Example: shift swap request', 2)
    t = d.add_table(rows=0, cols=2); t.style = 'Table Grid'; t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, f in enumerate(FIELDS):
        row = t.add_row().cells
        row[0].width, row[1].width = Cm(5), Cm(12)
        shade(row[0], '1D2B4F'); rr = row[0].paragraphs[0].add_run(f); rr.bold = True; rr.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        if vals:
            hint(vals[i], row[1].paragraphs[0])
        elif f == 'Area':
            row[1].paragraphs[0].add_run('☐ Work / job hunting    ☐ Study    ☐ Everyday life')
        elif f == 'Which tool worked best':
            row[1].paragraphs[0].add_run('☐ Claude (18+)    ☐ Copilot    ☐ Other: __________')
        elif f == 'The prompt':
            row[1].paragraphs[0].add_run('\n\n\n\n')
        else:
            row[1].paragraphs[0].add_run('\n')
    d.add_paragraph()


card(0, ['Asking my manager to swap a shift', 'Work / job hunting',
         'Write a [length] message to [who] asking for [what] because [reason]. [Extra detail, e.g. who can cover]. '
         'Tone: [friendly / formal]. Keep it under [number] words. Don\'t make up any details: leave a [gap] if you need something from me.',
         'Copilot on my phone (Claude gave a longer answer)',
         '"Make it shorter and start with the main point."',
         'Names, the day, the time and the reason are right. It sounds like me.',
         'Swapping my Saturday 8am shift for an exam',
         'Added "don\'t make up details": it had invented a reason the first time.'])
for n in range(1, 6):
    card(n)

d.add_heading('Check your prompts', 1)
t = d.add_table(rows=1, cols=6); t.style = 'Table Grid'
for i, h in enumerate(['Check', 'P1', 'P2', 'P3', 'P4', 'P5']):
    c = t.rows[0].cells[i]; shade(c, '1D2B4F'); r = c.paragraphs[0].add_run(h); r.bold = True; r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
for chk in ['Clear task, context, format and audience', 'No private information in it', 'Limits on length and style',
            'Tells the AI not to invent things (or to leave gaps)', 'Has a checking step', 'Tested, and it works']:
    row = t.add_row().cells; row[0].text = chk
    for c in row[1:]: c.text = '☐'
for row in t.rows:
    row.cells[0].width = Cm(9)
    for c in row.cells[1:]: c.width = Cm(1.6)

d.add_heading('Show it off', 1)
d.add_paragraph('"I use AI tools effectively and responsibly" is a real skill. Pick one prompt you could describe in a job interview: '
                'what it does, and how you check the results.')
hint('The prompt I\'d talk about, and why:')
d.add_paragraph('\n\n')
d.save(out); print(os.path.basename(out), os.path.getsize(out))
