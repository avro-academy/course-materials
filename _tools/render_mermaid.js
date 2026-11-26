const { chromium } = require('playwright'); const fs = require('fs');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ deviceScaleFactor: 2 });
  const lib = fs.readFileSync('node_modules/mermaid/dist/mermaid.min.js', 'utf8');
  for (const [src, out] of JSON.parse(process.argv[2])) {
    const code = fs.readFileSync(src, 'utf8');
    await p.setContent(`<html><body style="margin:0;background:#fff"><div id=g style="display:inline-block;padding:16px"></div></body></html>`);
    await p.addScriptTag({ content: lib });
    await p.evaluate(async (code) => { mermaid.initialize({ startOnLoad: false, theme: 'default', flowchart: { useMaxWidth: false } });
      const { svg } = await mermaid.render('m', code); document.getElementById('g').innerHTML = svg; }, code);
    await (await p.$('#g')).screenshot({ path: out });
  }
  await b.close();
})();
