import { test, expect } from '@playwright/test';
import { APP } from './app';

test.beforeEach(async ({ page }) => {
  await page.goto(APP);
});

test('the menu page loads', async ({ page }) => {
  await expect(page).toHaveTitle('Order Ahead · Corner Café');
  await expect(page.getByRole('heading', { name: 'Menu' })).toBeVisible();
});

test('REQ-1: prices show dollars and cents', async ({ page }) => {
  const flatWhite = page.getByRole('listitem').filter({ hasText: 'Flat white' });
  await expect(flatWhite).toContainText('$4.80');
});

test('REQ-2: the Drinks filter shows orange juice', async ({ page }) => {
  await page.getByRole('button', { name: 'Drinks' }).click();
  await expect(page.getByText('Orange juice')).toBeVisible();
});

test('REQ-3: search ignores capital letters', async ({ page }) => {
  await page.getByLabel('Search the menu').fill('latte');
  await expect(page.getByText('Latte', { exact: true })).toBeVisible();
});
