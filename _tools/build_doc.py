"""Build a single-column document PDF.
Usage: python3 _tools/build_doc.py <body.html> <out.pdf> "<Title>" "<Course name>"
"""
import html, os, subprocess, sys
body, out, title, course = sys.argv[1:5]
here = os.path.dirname(os.path.abspath(__file__))
css = open(os.path.join(here, 'doc.css')).read()
doc = f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>{html.escape(title)} · Avro Academy</title><style>{css}</style></head><body>
<header><h1>{html.escape(title)}</h1><p><strong>{html.escape(course)}</strong><br>Avro Academy · avro.academy</p></header>
{open(body).read()}
<footer>Avro Academy · {html.escape(course)} · Free forever</footer></body></html>"""
full = os.path.splitext(body)[0] + '.full.html'
open(full, 'w').write(doc)
subprocess.run(['node', os.path.join(here, 'pdf.js'), os.path.abspath(full), os.path.abspath(out)], check=True)
os.remove(full)
print(os.path.basename(out), subprocess.run(['pdfinfo', out], capture_output=True, text=True).stdout.split('Pages:')[1].split('\n')[0].strip(), 'pages')
