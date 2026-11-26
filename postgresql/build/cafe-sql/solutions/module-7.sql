-- Module 7: More powerful queries. Answers to the "Try it" questions.

-- Subqueries and WITH
SELECT first_name, hourly_rate
FROM staff
WHERE hourly_rate > (SELECT avg(hourly_rate) FROM staff);

WITH daily AS (
  SELECT ordered_at::date AS day, count(*) AS orders
  FROM orders
  WHERE ordered_at < '2026-04-01'
  GROUP BY day
)
SELECT round(avg(orders), 1) AS average_orders_per_day FROM daily;   -- 48.1

-- CASE and views
SELECT CASE
         WHEN price < 5 THEN 'Budget'
         WHEN price < 8 THEN 'Standard'
         ELSE 'Premium'
       END AS price_band,
       count(*) AS items
FROM menu_items
GROUP BY price_band
ORDER BY items DESC;

CREATE VIEW item_sales AS
SELECT m.name, coalesce(sum(oi.quantity), 0) AS sold
FROM menu_items m
LEFT JOIN order_items oi ON oi.menu_item_id = m.id
GROUP BY m.name;

SELECT * FROM item_sales ORDER BY sold DESC LIMIT 3;

-- Indexes and EXPLAIN
CREATE INDEX orders_ordered_at_idx ON orders (ordered_at);

EXPLAIN SELECT * FROM orders
WHERE ordered_at >= '2026-03-14' AND ordered_at < '2026-03-15';
-- Write the day as a range like this so the index can be used.
-- WHERE ordered_at::date = '2026-03-14' changes every value first, so it can't use it.

\d orders
