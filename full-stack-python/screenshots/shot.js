const { chromium } = require('playwright');
const U = 'http://localhost:5055';
(async () => { const b = await chromium.launch(); const ctx = await b.newContext({ viewport: { width: 1100, height: 700 }, deviceScaleFactor: 2 }); const p = await ctx.newPage();
  async function reg(u) { await p.goto(U + '/register'); await p.fill('input[name=username]', u); await p.fill('input[name=password]', 'coffee-time-42'); await p.click('form:not([action*=logout]) button');
    await p.goto(U + '/login'); await p.fill('input[name=username]', u); await p.fill('input[name=password]', 'coffee-time-42'); await p.click('form:not([action*=logout]) button'); }
  await reg('alex');
  const d = new Date(); d.setDate(d.getDate() + ((6 - d.getDay() + 7) % 7 || 7)); const day = d.toISOString().slice(0, 10);
  await p.goto(U + '/shifts/new'); await p.fill('input[name=day]', day); await p.fill('input[name=start]', '07:00'); await p.fill('input[name=finish]', '13:00');
  await p.selectOption('select[name=role]', 'Barista'); await p.fill('input[name=note]', 'Includes the morning rush'); await p.click('form:not([action*=logout]) button');
  await p.click('button:has-text("Log out")');
  await reg('sam'); await p.goto(U + '/'); await p.waitForTimeout(500);
  await p.screenshot({ path: 'board.png', fullPage: true });
  await p.click('text=Take this shift'); await p.waitForTimeout(1200);
  await p.screenshot({ path: 'claimed.png', fullPage: true });
  await b.close(); })();
