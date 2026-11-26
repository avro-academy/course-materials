-- Module 4: Answering money questions. Answers to the "Try it" questions.

-- Categorise the spending
SELECT day, description, amount, category
FROM transactions
WHERE description LIKE '%PAGEPLUS%';

INSERT INTO rules (pattern, category, priority) VALUES ('%VALUEMART%', 'Groceries', 5);
SELECT 'VALUEMART' LIKE '%VALUEMART%';   -- 1: it matches
SELECT r.pattern, r.category
FROM rules r
WHERE 'VALUEMART' LIKE r.pattern
ORDER BY r.priority;

-- Monthly reports and the budget
SELECT strftime('%Y-%m', day) AS month, round(-sum(amount), 2) AS eating_out
FROM transactions
WHERE category = 'Eating out'
GROUP BY month;

SELECT round(avg(-amount), 2) AS average_coffee, count(*) AS coffees
FROM transactions
WHERE description = 'BEAN THERE CAFE';

-- Views and sharing results
CREATE VIEW monthly_summary AS
SELECT strftime('%Y-%m', day) AS month,
       round(sum(CASE WHEN amount > 0 THEN amount ELSE 0 END), 2) AS money_in,
       round(sum(CASE WHEN amount < 0 THEN -amount ELSE 0 END), 2) AS money_out
FROM transactions
GROUP BY month;

SELECT * FROM monthly_summary;

.headers on
.mode csv
.once march.csv
SELECT * FROM transactions WHERE day BETWEEN '2026-03-01' AND '2026-03-31' ORDER BY id;
.mode box
