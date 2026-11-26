"""sheet_shot.py book.xlsx out_dir spec.json
Renders worksheet ranges as a spreadsheet-style HTML grid (column letters, row numbers,
cell fills, bold, number formats, column widths) and screenshots each one with Playwright.
The workbook must hold cached values (open and save it in LibreOffice first).
spec: [{"sheet": "...", "out": "x.png", "rows": 25, "filter": {"col": "E", "not": "Active"}}]"""
import datetime, html, json, os, subprocess, sys
import openpyxl
from openpyxl.utils import get_column_letter, column_index_from_string

book, out_dir, spec = sys.argv[1], sys.argv[2], json.load(open(sys.argv[3]))
wb = openpyxl.load_workbook(book, data_only=True)

def fmt(v, nf):
    if v is None: return ""
    if isinstance(v, (datetime.datetime, datetime.date)): return f"{v.day}/{v.month:02d}/{v.year}"
    if isinstance(v, (int, float)) and not isinstance(v, bool):
        if "%" in nf:
            d = nf.split("%")[0].count("0") - 1
            return f"{v*100:.{max(d,0)}f}%"
        if "$" in nf:
            s = f"${abs(v):,.2f}" if ".00" in nf else f"${abs(v):,.0f}"
            return "-" + s if v < 0 else s
        if "#,##0" in nf: return f"{v:,.0f}" if ".0" not in nf else f"{v:,.2f}"
        if nf == "0": return f"{v:.0f}"
        if isinstance(v, float): return f"{v:.2f}".rstrip("0").rstrip(".")
    return str(v)

def colour(c):
    try:
        if c and c.type == "rgb" and c.rgb and c.rgb not in ("00000000",) : return "#" + c.rgb[-6:]
    except Exception: pass
    return None

pages = []
for s in spec:
    ws = wb[s["sheet"]]
    ncol = s.get("cols", ws.max_column); nrow = min(s.get("rows", ws.max_row), ws.max_row)
    rows = list(range(1, nrow + 1))
    if "filter" in s:
        ci = column_index_from_string(s["filter"]["col"])
        rows = [1] + [r for r in range(2, ws.max_row + 1) if ws.cell(r, ci).value != s["filter"]["not"]]
    widths = []
    for c in range(1, ncol + 1):
        w = ws.column_dimensions[get_column_letter(c)].width or 10
        widths.append(int(w * 7.2 + 10))
    h = ["<table class=g><tr><th class=corner></th>"]
    h += [f"<th style='width:{w}px'>{get_column_letter(i+1)}{' ▾' if 'filter' in s or ws.auto_filter.ref else ''}</th>" for i, w in enumerate(widths)]
    h.append("</tr>")
    for r in rows:
        h.append(f"<tr><th class=rn>{r}</th>")
        for c in range(1, ncol + 1):
            cell = ws.cell(r, c); st = []
            bg = colour(cell.fill.fgColor) if cell.fill and cell.fill.fill_type == "solid" else None
            if bg: st.append(f"background:{bg}")
            if cell.font and cell.font.b: st.append("font-weight:700")
            fc = colour(cell.font.color) if cell.font and cell.font.color else None
            if fc and fc.lower() != "#000000": st.append(f"color:{fc}")
            v = cell.value
            if isinstance(v, (int, float)) and not isinstance(v, bool) or isinstance(v, (datetime.date,)): st.append("text-align:right")
            if cell.alignment and cell.alignment.wrap_text: st.append("white-space:normal")
            h.append(f"<td style='{';'.join(st)}'>{html.escape(fmt(v, cell.number_format))}</td>")
        h.append("</tr>")
    h.append("</table>")
    tabs = "".join(f"<span class='tab{' on' if n == s['sheet'] else ''}'>{html.escape(n)}</span>" for n in wb.sheetnames)
    pages.append((s["out"], f"<div class=wrap id=w>{''.join(h)}<div class=tabs>{tabs}</div></div>"))

css = """body{margin:0;background:#fff;font:13px Arial,Helvetica,sans-serif;color:#202124}
.wrap{display:inline-block;padding:0}
table.g{border-collapse:collapse;table-layout:fixed}
.g th{background:#f3f3f3;color:#5f6368;font-weight:400;border:1px solid #d6d6d6;height:21px;font-size:12px}
.g th.rn{width:40px}.g th.corner{width:40px}
.g td{border:1px solid #e2e2e2;padding:2px 5px;height:19px;white-space:nowrap;overflow:hidden;text-overflow:clip}
.tabs{display:flex;gap:2px;background:#f3f3f3;border-top:1px solid #d6d6d6;padding:4px 6px;overflow:hidden;white-space:nowrap}
.tab{padding:4px 12px;font-size:12px;color:#5f6368}.tab.on{background:#fff;color:#188038;font-weight:700;border-bottom:2px solid #188038}"""
js = """const { chromium } = require('playwright'); const fs = require('fs');
(async () => { const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 2400, height: 900 }, deviceScaleFactor: 2 });
for (const [out, body] of JSON.parse(fs.readFileSync(process.argv[2], 'utf8'))) {
  await p.setContent(`<style>${process.argv[3]}</style>` + body);
  await (await p.$('#w')).screenshot({ path: out }); }
await b.close(); })();"""
os.makedirs(out_dir, exist_ok=True)
jp = os.path.join(out_dir, "_pages.json"); json.dump([(os.path.join(out_dir, o), b) for o, b in pages], open(jp, "w"))
sp = os.path.join(out_dir, "_shot.js"); open(sp, "w").write(js)
subprocess.run(["node", sp, jp, css], check=True)
for o, _ in pages: print(o)
