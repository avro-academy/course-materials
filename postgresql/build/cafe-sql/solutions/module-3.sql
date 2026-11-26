-- Module 3: Summaries. Answers to the "Try it" questions.

-- Counting and totals
SELECT count(*) AS no_email FROM customers WHERE email IS NULL;

SELECT sum(quantity) AS items_sold FROM order_items;

SELECT max(hourly_rate) AS highest, round(avg(hourly_rate), 2) AS average
FROM staff;

-- GROUP BY and HAVING
SELECT role, count(*) FROM staff GROUP BY role ORDER BY role;

SELECT customer_id, count(*) AS orders
FROM orders
WHERE customer_id IS NOT NULL
GROUP BY customer_id
ORDER BY orders DESC
LIMIT 5;

SELECT menu_item_id, sum(quantity * unit_price) AS revenue
FROM order_items
GROUP BY menu_item_id
HAVING sum(quantity * unit_price) > 1000
ORDER BY revenue DESC;

-- Dates, times and text
SELECT ordered_at::date AS day, count(*) AS orders
FROM orders
WHERE ordered_at::date BETWEEN '2026-03-01' AND '2026-03-07'
GROUP BY day
ORDER BY day;

SELECT count(*) AS before_8am FROM orders WHERE extract(hour FROM ordered_at) < 8;

SELECT name, extract(year FROM joined_on) AS year_joined FROM customers;
