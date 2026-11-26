import { test, expect } from '@playwright/test';
import { APP } from './app';

test.beforeEach(async ({ page }) => {
  await page.goto(APP);
});

test('REQ-4: a large latte costs $1.00 more', async ({ page }) => {
  await page.getByRole('button', { name: 'Add Latte' }).click();
  await page.getByText('Large').click();
  await page.getByRole('button', { name: 'Add to order' }).click();
  await expect(page.locator('#total')).toHaveText('$5.80');
});

test('REQ-5: a quantity of 11 is not allowed', async ({ page }) => {
  await page.getByRole('button', { name: 'Add Banana bread' }).click();
  await page.getByLabel('Quantity').fill('11');
  await page.getByRole('button', { name: 'Add to order' }).click();
  await expect(page.getByText('Choose a quantity from 1 to 10.')).toBeVisible();
  await expect(page.locator('#total')).toHaveText('$0.00');
});

test('REQ-7: changing a quantity updates the total', async ({ page }) => {
  await page.getByRole('button', { name: 'Add Banana bread' }).click();
  await page.getByRole('button', { name: 'Add to order' }).click();
  await page.getByLabel('Quantity of Banana bread').fill('3');
  await page.getByLabel('Quantity of Banana bread').press('Tab');
  await expect(page.locator('#total')).toHaveText('$16.50');
});

test('REQ-8: the discount code works in lower case', async ({ page }) => {
  await page.getByRole('button', { name: 'Add Banana bread' }).click();
  await page.getByRole('button', { name: 'Add to order' }).click();
  await page.getByLabel('Discount code').fill('student10');
  await page.getByRole('button', { name: 'Apply' }).click();
  await expect(page.locator('#total')).toHaveText('$4.95');
});
