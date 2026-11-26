const { chromium } = require('playwright');
(async () => { const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1100, height: 656 }, deviceScaleFactor: 2 });
  await p.goto(process.argv[2]); await p.screenshot({ path: process.argv[3] }); await b.close(); })();
