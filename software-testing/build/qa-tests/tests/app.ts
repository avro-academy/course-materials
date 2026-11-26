import path from 'path';

// Where the app is: the order-ahead folder next to this qa-tests folder.
// To test another copy, set APP_DIR, e.g. APP_DIR=order-ahead-fixed npx playwright test
const appDir = process.env.APP_DIR ?? 'order-ahead';
export const APP = 'file://' + path.join(__dirname, '..', '..', appDir, 'index.html');
