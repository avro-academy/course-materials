-- Module 8: Safe and useful. Answers to the "Try it" questions and the capstone.

-- Users and permissions
\du

GRANT SELECT ON shifts TO reporter;
SET ROLE reporter;
SELECT count(*) FROM shifts;                -- works
DELETE FROM shifts;                         -- ERROR:  permission denied for table shifts
RESET ROLE;

-- Backups and exports (the item_sales view is from Module 7)
\copy (SELECT * FROM item_sales ORDER BY sold DESC LIMIT 5) TO 'top-items.csv' WITH (FORMAT csv, HEADER)

-- Capstone: the monthly report
-- Run \i cafe.sql first if you want these to match a fresh database exactly.
-- Every query only looks at March (ordered_at < '2026-04-01').

-- Takings
SELECT count(DISTINCT o.id) AS orders, sum(oi.quantity * oi.unit_price) AS takings
FROM orders o
JOIN order_items oi ON oi.order_id = o.id
WHERE o.ordered_at < '2026-04-01';
-- 1492 orders, 16489.00

-- Average order
WITH order_totals AS (
  SELECT o.id, sum(oi.quantity * oi.unit_price) AS total
  FROM orders o
  JOIN order_items oi ON oi.order_id = o.id
  WHERE o.ordered_at < '2026-04-01'
  GROUP BY o.id
)
SELECT round(avg(total), 2) AS average_order FROM order_totals;
-- 11.05

-- Best sellers by money taken
SELECT m.name, c.name AS category, sum(oi.quantity * oi.unit_price) AS revenue
FROM order_items oi
JOIN orders o ON o.id = oi.order_id
JOIN menu_items m ON m.id = oi.menu_item_id
JOIN categories c ON c.id = m.category_id
WHERE o.ordered_at < '2026-04-01'
GROUP BY m.name, c.name
ORDER BY revenue DESC
LIMIT 3;

-- Weekends
SELECT round(100.0 * count(*) FILTER (WHERE extract(isodow FROM ordered_at) IN (6, 7))
             / count(*), 1) AS weekend_percent
FROM orders
WHERE ordered_at < '2026-04-01';
-- Without FILTER: sum(CASE WHEN extract(isodow FROM ordered_at) IN (6, 7) THEN 1 ELSE 0 END)

-- Cash for each week
SELECT date_trunc('week', o.ordered_at)::date AS week_starting,
       sum(oi.quantity * oi.unit_price) AS cash
FROM orders o
JOIN order_items oi ON oi.order_id = o.id
WHERE o.payment = 'Cash' AND o.ordered_at < '2026-04-01'
GROUP BY week_starting
ORDER BY week_starting;
-- The first "week" starts on Monday 23 February: 1 March was a Sunday.

-- Loyalty: top 3 members and their last visit
SELECT cu.name,
       sum(oi.quantity * oi.unit_price) AS spent,
       max(o.ordered_at)::date AS last_visit
FROM customers cu
JOIN orders o ON o.customer_id = cu.id
JOIN order_items oi ON oi.order_id = o.id
WHERE o.ordered_at < '2026-04-01'
GROUP BY cu.name
ORDER BY spent DESC
LIMIT 3;
