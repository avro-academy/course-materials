# qa-tests-answers

The finished Playwright tests from Module 7 of Software Testing Foundations. Unzip the answer key into the same folder as order-ahead so this folder sits next to order-ahead and order-ahead-fixed.

```bash
npm install
npx playwright install chromium
npx playwright test                              # tests ../order-ahead (most fail: they find the bugs)
APP_DIR=order-ahead-fixed npx playwright test    # tests ../order-ahead-fixed (all pass)
```

On Windows PowerShell: `$env:APP_DIR="order-ahead-fixed"; npx playwright test`
