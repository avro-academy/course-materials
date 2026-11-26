-- Module 2: Asking questions with SELECT. Answers to the "Try it" questions.

-- Your first queries
SELECT first_name, role, hourly_rate FROM staff;

SELECT name, phone FROM customers LIMIT 5;

SELECT name, price * 3 AS three_of_them FROM menu_items;

-- Filtering with WHERE
SELECT name, price FROM menu_items WHERE vegetarian = false;
-- (or: WHERE NOT vegetarian)

SELECT name FROM customers WHERE name LIKE 'A%';

SELECT id, ordered_at, payment
FROM orders
WHERE payment = 'Cash' AND staff_id = 5
LIMIT 5;

SELECT name FROM menu_items WHERE available = false;

-- Sorting and removing duplicates
SELECT first_name, started_on FROM staff ORDER BY started_on DESC;

SELECT name, price
FROM menu_items
WHERE category_id IN (1, 2, 3)
ORDER BY price
LIMIT 3;

SELECT name, joined_on FROM customers ORDER BY joined_on DESC LIMIT 5;
