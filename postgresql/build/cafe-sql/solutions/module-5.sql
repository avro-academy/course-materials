-- Module 5: Changing data. Answers to the "Try it" questions.
-- These change the database. Run \i cafe.sql any time to start again.

-- Adding rows with INSERT
INSERT INTO customers (name, email, phone)
VALUES ('Your Name', 'you@example.com', '0400 123 456')
RETURNING id;

-- The lesson added the Cakes category. Find its id...
SELECT id FROM categories WHERE name = 'Cakes';
-- ...then use it (5 if you followed the lesson):
INSERT INTO menu_items (name, category_id, price, vegetarian)
VALUES ('Carrot cake', 5, 6.00, true);
-- Or let a subquery find the id for you:
-- VALUES ('Carrot cake', (SELECT id FROM categories WHERE name = 'Cakes'), 6.00, true);

-- Changing and removing rows
SELECT name, price FROM menu_items WHERE name = 'Banana bread';   -- check first: 1 row
UPDATE menu_items SET price = 5.80 WHERE name = 'Banana bread';   -- UPDATE 1

DELETE FROM customers WHERE email = 'you@example.com';            -- DELETE 1

-- Transactions
BEGIN;
DELETE FROM orders WHERE payment = 'Cash';   -- their order_items go too (ON DELETE CASCADE)
SELECT count(*) FROM orders;                 -- 1492 - 288 = 1204 (or 1205 after the April order)
ROLLBACK;
SELECT count(*) FROM orders;                 -- back to 1492 (or 1493)

BEGIN;
UPDATE staff SET hourly_rate = round(hourly_rate * 1.03, 2);
SELECT first_name, hourly_rate FROM staff ORDER BY id;
ROLLBACK;
