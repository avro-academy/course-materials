-- Module 4: Joins. Answers to the "Try it" questions.

-- Keys: how tables connect
SELECT * FROM menu_items WHERE id = 7;

SELECT staff_id FROM orders WHERE id = 10;
SELECT first_name, last_name FROM staff WHERE id = 3;   -- the staff_id you got: Jordan

-- Joining tables
SELECT o.id, o.ordered_at, s.first_name
FROM orders o
JOIN staff s ON s.id = o.staff_id
ORDER BY o.id
LIMIT 5;

SELECT m.name, m.price
FROM menu_items m
JOIN categories c ON c.id = m.category_id
WHERE c.name = 'Food' AND m.vegetarian = true;

SELECT cu.name, count(*) AS orders
FROM orders o
JOIN customers cu ON cu.id = o.customer_id
GROUP BY cu.name
ORDER BY orders DESC
LIMIT 1;

-- LEFT JOIN and joining many tables
SELECT s.first_name, coalesce(sum(oi.quantity * oi.unit_price), 0) AS takings
FROM staff s
LEFT JOIN orders o ON o.staff_id = s.id
LEFT JOIN order_items oi ON oi.order_id = o.id
GROUP BY s.first_name
ORDER BY takings DESC;

SELECT o.ordered_at::date AS day, m.name AS item, oi.quantity
FROM customers cu
JOIN orders o ON o.customer_id = cu.id
JOIN order_items oi ON oi.order_id = o.id
JOIN menu_items m ON m.id = oi.menu_item_id
WHERE cu.name = 'Aisha Tran'
  AND o.ordered_at >= '2026-03-01' AND o.ordered_at < '2026-03-08'
ORDER BY o.ordered_at;
