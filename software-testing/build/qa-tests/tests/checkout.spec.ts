import { test, expect, type Page } from '@playwright/test';
import { APP } from './app';

async function orderBananaBread(page: Page, name: string, phone: string) {
  await page.getByRole('button', { name: 'Add Banana bread' }).click();
  await page.getByRole('button', { name: 'Add to order' }).click();
  await page.getByRole('button', { name: 'Go to checkout' }).click();
  await page.getByLabel('Your name').fill(name);
  await page.locator('#phone').fill(phone);
  await page.getByRole('button', { name: 'Place order' }).click();
}

test.beforeEach(async ({ page }) => {
  await page.goto(APP);
});

test('REQ-10: you cannot check out an empty order', async ({ page }) => {
  await page.getByRole('button', { name: 'Go to checkout' }).click();
  await expect(page.getByText('Add something to your order first.')).toBeVisible();
});

test('REQ-11: names can have an apostrophe', async ({ page }) => {
  await orderBananaBread(page, "Sam O'Brien", '0412345678');
  await expect(page.getByRole('heading', { name: 'Order placed' })).toBeVisible();
});

test('REQ-12: phone numbers can have spaces', async ({ page }) => {
  await orderBananaBread(page, 'Sam Lee', '0412 345 678');
  await expect(page.getByRole('heading', { name: 'Order placed' })).toBeVisible();
});

test('REQ-15: each order gets a new number', async ({ page }) => {
  await orderBananaBread(page, 'Sam Lee', '0412345678');
  const first = await page.locator('#order-number').textContent();
  await page.getByRole('button', { name: 'Start a new order' }).click();
  await orderBananaBread(page, 'Sam Lee', '0412345678');
  await expect(page.locator('#order-number')).not.toHaveText(first!);
});
