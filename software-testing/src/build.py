"""Builds order-ahead (with the 20 planted bugs) and order-ahead-fixed from the templates in src/.
Lines ending in //@B are only in the buggy app, //@F only in the fixed app."""
import os, re, shutil
here = os.path.dirname(os.path.abspath(__file__))
out = os.path.join(here, '..', 'build')
def strip(text, keep):
    lines = []
    for line in text.splitlines():
        m = re.search(r'\s*//@([BF])\s*$', line)
        if m:
            if m.group(1) != keep: continue
            line = line[:m.start()]
        lines.append(line)
    return '\n'.join(lines) + '\n'
MOBILE_BUGGY = """@media (max-width: 760px) {
  .layout { grid-template-columns: 1fr; padding: 12px; }
  .totals { min-width: 420px; }
}"""
MOBILE_FIXED = """@media (max-width: 760px) {
  .layout { grid-template-columns: 1fr; padding: 12px; }
}
:focus-visible { outline: 3px solid #b4532a; outline-offset: 2px; }"""
for keep, name in (('B', 'order-ahead'), ('F', 'order-ahead-fixed')):
    d = os.path.join(out, name); shutil.rmtree(d, ignore_errors=True); os.makedirs(d)
    js = strip(open(os.path.join(here, 'app.tpl.js')).read(), keep)
    html = open(os.path.join(here, 'index.tpl.html')).read()
    html = html.replace('@@PHONE_LABEL@@', '      <label for="phone">Mobile number</label>' if keep == 'F' else '      <p class="field-hint">Mobile number</p>')
    html = html.replace('@@PHONE_PLACEHOLDER@@', 'placeholder="0412 345 678"' if keep == 'F' else 'placeholder="Mobile number"')
    html = html.replace('@@NOTES_MAX@@', '200' if keep == 'F' else '210')
    css = open(os.path.join(here, 'style.tpl.css')).read().replace('@@MUTED@@', '#6d5d4f').replace('@@MOBILE_CSS@@', MOBILE_FIXED if keep == 'F' else MOBILE_BUGGY + '\n.field-hint { font-weight: 600; margin: 10px 0 4px; }')
    open(os.path.join(d, 'app.js'), 'w').write(js)
    open(os.path.join(d, 'index.html'), 'w').write(html)
    open(os.path.join(d, 'style.css'), 'w').write(css)
print('built')
