"""Build a cheat sheet PDF from a body fragment.

Usage: python3 _tools/build_cheatsheet.py <fragment.html> <out.pdf> "<Title (last word coloured)>" "<Course name>"
The fragment holds <section> blocks (class "", "coral" or "amber"); they flow into 3 columns.
"""
import html, os, subprocess, sys
frag, out, title, course = sys.argv[1:5]
here = os.path.dirname(os.path.abspath(__file__))
css = open(os.path.join(here, 'cheatsheet.css')).read()
words = title.rsplit(' ', 2)
head = html.escape(' '.join(words[:-2])) + ' <span>' + html.escape(' '.join(words[-2:])) + '</span>' if len(words) > 2 else html.escape(title)
doc = f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>{html.escape(title)} · Avro Academy</title><style>{css}</style></head><body>
<header><h1>{head}</h1><p><strong>{html.escape(course)}</strong><br>Avro Academy · avro.academy</p></header>
<div class="cols">{open(frag).read()}</div>
<footer>Avro Academy · {html.escape(course)} · Free forever</footer></body></html>"""
full = os.path.splitext(frag)[0] + '.full.html'
open(full, 'w').write(doc)
subprocess.run(['node', os.path.join(here, 'pdf.js'), os.path.abspath(full), os.path.abspath(out)], check=True)
os.remove(full)
print(subprocess.run(['pdfinfo', out], capture_output=True, text=True).stdout.split('Pages:')[1].split('\n')[0].strip(), 'pages')
