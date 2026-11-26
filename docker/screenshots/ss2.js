const { chromium } = require('playwright');
const U = 'http://localhost:5000';
(async () => { const b = await chromium.launch(); const ctx = await b.newContext({ viewport: { width: 1000, height: 596 }, deviceScaleFactor: 2 }); const p = await ctx.newPage();
  async function reg(u) { await p.goto(U + '/register'); await p.fill('input[name=username]', u); await p.fill('input[name=password]', 'coffee-time-42'); await p.click('form:not([action*=logout]) button');
    await p.goto(U + '/login'); await p.fill('input[name=username]', u); await p.fill('input[name=password]', 'coffee-time-42'); await p.click('form:not([action*=logout]) button'); }
  await reg('priya');
  const d = new Date(); d.setDate(d.getDate() + ((6 - d.getDay() + 7) % 7 || 7)); const day = d.toISOString().slice(0, 10);
  await p.goto(U + '/shifts/new'); await p.fill('input[name=day]', day); await p.fill('input[name=start]', '07:00'); await p.fill('input[name=finish]', '13:00');
  await p.selectOption('select[name=role]', 'Barista'); await p.fill('input[name=note]', 'Includes the morning rush'); await p.click('form:not([action*=logout]) button');
  const d2 = new Date(d); d2.setDate(d2.getDate()+1); await p.goto(U + '/shifts/new'); await p.fill('input[name=day]', d2.toISOString().slice(0,10)); await p.fill('input[name=start]', '10:00'); await p.fill('input[name=finish]', '15:00'); await p.selectOption('select[name=role]', {index: 2}); await p.fill('input[name=note]', 'Lunch service'); await p.click('form:not([action*=logout]) button');
  await p.click('button:has-text("Log out")');
  await reg('sam'); await p.goto(U + '/'); await p.waitForTimeout(500); await p.setViewportSize({width:1000,height:596});
  await p.screenshot({ path: 'board.png', fullPage: false });
  await b.close(); return;
  await p.screenshot({ path: 'claimed.png', fullPage: false });
  await b.close(); })();
