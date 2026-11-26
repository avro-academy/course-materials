"""Makes the seven Corner Café documents in ../docs (run from anywhere): 4 PDFs, 2 Word files and a Markdown file.
Needs: playwright (with Chromium), python-docx."""
import html, os, sys
from docx import Document
from playwright.sync_api import sync_playwright

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import docs_content as D

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "docs")
os.makedirs(OUT, exist_ok=True)

CSS = """
@page { size: A4; margin: 26mm 24mm 24mm 24mm; }
body { font-family: 'DejaVu Serif'; font-size: 10.2pt; line-height: 1.45; color: #1c2430; }
.page { page-break-after: always; }
.page:last-child { page-break-after: auto; }
h1 { font-family: 'DejaVu Sans'; font-size: 15pt; color: #14284b; margin: 0 0 8pt; }
h2 { font-family: 'DejaVu Sans'; font-size: 11.5pt; color: #14284b; margin: 14pt 0 4pt; }
h1 + h2 { margin-top: 6pt; }
p { margin: 0 0 8pt; }
p.lead { font-family: 'DejaVu Sans'; font-weight: bold; color: #14284b; font-size: 12pt; }
ul { margin: 0 0 8pt; padding-left: 16pt; }
li { margin-bottom: 3pt; }
table { border-collapse: collapse; width: 100%; margin: 4pt 0 10pt; font-size: 9.5pt; }
th, td { border: 0.6pt solid #b8c0cc; padding: 4pt 6pt; text-align: left; vertical-align: top; }
th { background: #e9eef5; font-family: 'DejaVu Sans'; }
.cover { padding-top: 70mm; text-align: center; }
.cover .c0 { font-family: 'DejaVu Sans'; font-size: 14pt; color: #e8614d; letter-spacing: 1pt; margin-bottom: 6pt; }
.cover .c1 { font-family: 'DejaVu Sans'; font-size: 30pt; font-weight: bold; color: #14284b; margin-bottom: 18pt; }
.cover .c2 { font-size: 12pt; margin-bottom: 40pt; }
.cover div { margin-bottom: 6pt; }
.toc div { margin: 0 0 3pt 8pt; }
"""

HEADER = ('<div style="width:100%;font-family:\'DejaVu Sans\';font-size:8pt;color:#6b7686;padding:0 24mm;'
          'text-align:right">Corner Café Staff Handbook</div>')
FOOTER = ('<div style="width:100%;font-family:\'DejaVu Sans\';font-size:8pt;color:#6b7686;text-align:center">'
          'Page <span class="pageNumber"></span> of <span class="totalPages"></span></div>')


def block_html(kind, value):
    if kind == "cover":
        return '<div class="cover">' + "".join(f'<div class="c{i if i < 3 else 3}">{html.escape(v)}</div>'
                                               for i, v in enumerate(value)) + "</div>"
    if kind == "table":
        head, *rows = value
        return ("<table><tr>" + "".join(f"<th>{html.escape(c)}</th>" for c in head) + "</tr>"
                + "".join("<tr>" + "".join(f"<td>{html.escape(c)}</td>" for c in r) + "</tr>" for r in rows) + "</table>")
    if kind == "toc":
        return '<div class="toc">' + "".join(f"<div>{html.escape(v)}</div>" for v in value) + "</div>"
    if kind == "lead":
        return f'<p class="lead">{html.escape(value)}</p>'
    return f"<{kind}>{html.escape(value)}</{kind}>"


def page_html(blocks):
    out, items = [], []
    for kind, value in blocks:
        if kind == "li":
            items.append(f"<li>{html.escape(value)}</li>")
            continue
        if items:
            out.append("<ul>" + "".join(items) + "</ul>")
            items = []
        out.append(block_html(kind, value))
    if items:
        out.append("<ul>" + "".join(items) + "</ul>")
    return '<section class="page">' + "".join(out) + "</section>"


def make_pdf(browser, name, pages, title, handbook):
    doc = f"<!doctype html><html><head><meta charset='utf-8'><title>{title}</title><style>{CSS}</style></head><body>"
    doc += "".join(page_html(p) for p in pages) + "</body></html>"
    page = browser.new_page()
    page.set_content(doc)
    page.pdf(path=os.path.join(OUT, name), format="A4", display_header_footer=True,
             header_template=HEADER if handbook else "<span></span>", footer_template=FOOTER,
             margin={"top": "26mm", "bottom": "24mm", "left": "24mm", "right": "24mm"})
    page.close()


def make_docx(name, blocks):
    d = Document()
    for kind, text in blocks:
        if kind == "title":
            d.add_heading(text, level=0)
        elif kind == "h":
            d.add_heading(text, level=1)
        else:
            d.add_paragraph(text)
    d.core_properties.title = blocks[0][1]
    d.core_properties.author = "Corner Café"
    d.save(os.path.join(OUT, name))


with sync_playwright() as p:
    browser = p.chromium.launch(executable_path=os.environ.get("CHROMIUM") or None)
    make_pdf(browser, "Corner-Cafe-Staff-Handbook-2026.pdf", D.HANDBOOK_2026, "Corner Café Staff Handbook (2026)", True)
    make_pdf(browser, "Corner-Cafe-Staff-Handbook-2024.pdf", D.HANDBOOK_2024, "Corner Café Staff Handbook (2024)", True)
    make_pdf(browser, "Food-Safety-Program.pdf", D.FOOD_SAFETY, "Corner Café Food Safety Program", False)
    make_pdf(browser, "Espresso-Machine-Guide.pdf", D.ESPRESSO, "Corner Café Espresso Machine Guide", False)
    browser.close()
make_docx("Refunds-and-Complaints-Policy.docx", D.REFUNDS)
make_docx("Privacy-Policy.docx", D.PRIVACY)
with open(os.path.join(OUT, "Staff-FAQ.md"), "w", encoding="utf-8") as f:
    f.write(D.FAQ)
print("Made", len(os.listdir(OUT)), "documents in", os.path.abspath(OUT))
