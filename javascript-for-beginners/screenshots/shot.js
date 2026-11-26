const { chromium } = require('playwright'); const path = require('path');
const J = process.argv[2];
(async () => { const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 900, height: 900 }, deviceScaleFactor: 2 });
  await p.goto('file://' + path.join(J, 'pay-calculator/finished/index.html'));
  await p.fill('#hours', '6'); await p.selectOption('#day', 'Saturday'); await p.click('#calculate'); await p.waitForTimeout(200);
  await p.screenshot({ path: 'pay.png', fullPage: true });
  await p.goto('file://' + path.join(J, 'todo-list/finished/index.html'));
  for (const t of ['Wipe tables', 'Restock the milk fridge', 'Empty the bins', 'Count the till']) { await p.fill('#task-input', t); await p.press('#task-input', 'Enter'); }
  await p.locator('#task-list input[type=checkbox]').first().check(); await p.waitForTimeout(200);
  await p.screenshot({ path: 'todo.png', fullPage: true });
  await b.close(); })();
