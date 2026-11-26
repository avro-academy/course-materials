// Screenshots of the MCP Inspector. Usage: node insp.js <inspector url with token>  (start the Inspector in src/s2 after python seed.py)
const { chromium } = require('playwright');
const [url] = process.argv.slice(2);
async function shoot(p, script, tool, args, out) {
  const u = new URL(url); u.searchParams.set('transport', 'stdio'); u.searchParams.set('serverCommand', 'python'); u.searchParams.set('serverArgs', script);
  await p.goto(u.toString()); await p.waitForTimeout(1500);
  await p.getByRole('button', { name: /^Connect$/ }).click();
  await p.getByRole('tab', { name: 'Tools' }).click({ timeout: 20000 });
  await p.getByRole('button', { name: /List Tools/ }).click();
  await p.getByText(tool, { exact: true }).first().click();
  for (const [k, v] of Object.entries(args)) await p.locator('#' + k).fill(v);
  await p.getByRole('button', { name: /Run Tool/ }).click(); await p.waitForTimeout(2000);
  // Keep the shot on the call: hide the output schema box, show the result.
  await p.evaluate(() => {
    for (const el of document.querySelectorAll('h4, span, div')) {
      const t = el.childNodes[0] && el.childNodes[0].textContent;
      if (t && t.trim() === 'Output Schema:') { el.closest('.bg-gray-50, .rounded, .p-4')?.style.setProperty('display', 'none'); }
    }
  });
  await p.locator('pre, code').last().evaluate(el => el.scrollIntoView({ block: 'end' }));
  await p.waitForTimeout(300);
  await p.screenshot({ path: out });
  await p.getByRole('button', { name: /Disconnect/ }).click().catch(() => {});
}
(async () => { const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1625, height: 1025 }, deviceScaleFactor: 0.8 });
  await shoot(p, 'hello.py', 'opening_time', { day: 'Saturday' }, 'mcp-inspector-hello.png');
  await shoot(p, 'server.py', 'booking_times', { date: '2026-11-28', people: '2', time: '10:00' }, 'mcp-inspector-booking.png');
  await b.close(); })().catch(e => { console.error(e.message); process.exit(1); });
