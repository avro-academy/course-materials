-- Module 2: Getting data in. Answers to the "Try it" questions.

-- Import a CSV file (raw_jan_feb)
SELECT * FROM raw_jan_feb WHERE Description LIKE '%PAYROLL%';
SELECT count(*) FROM raw_jan_feb WHERE Description LIKE '%PAYROLL%';   -- 5

SELECT Description, count(*) AS times
FROM raw_jan_feb
GROUP BY Description
ORDER BY times DESC
LIMIT 3;

-- Clean it into a proper table (transactions)
SELECT day, description, amount
FROM transactions
ORDER BY amount
LIMIT 5;

SELECT round(-sum(amount), 2) AS spent_at_bean_there
FROM transactions
WHERE description = 'BEAN THERE CAFE';

-- Duplicates from overlapping files
INSERT INTO transactions (day, description, amount, balance)
VALUES ('2026-01-01', 'CORNER CAFE PAYROLL', 688.75, 1501.15);
-- Runtime error: UNIQUE constraint failed:
--   transactions.day, transactions.description, transactions.amount, transactions.balance
-- Nothing is added.

SELECT * FROM transactions
WHERE day = '2026-02-10' AND description = 'BEAN THERE CAFE' AND amount = -5;   -- 2 rows
