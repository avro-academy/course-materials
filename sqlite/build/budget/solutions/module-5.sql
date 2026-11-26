-- Module 5: Python and beyond. Answers to the "Try it" questions and the capstone.

-- SQLite from Python: check the script's February numbers
SELECT round(sum(CASE WHEN amount > 0 THEN amount ELSE 0 END), 2) AS money_in,
       round(sum(CASE WHEN amount < 0 THEN -amount ELSE 0 END), 2) AS money_out
FROM transactions
WHERE day BETWEEN '2026-02-01' AND '2026-02-28';
-- 1776.85 in, 1717.5 out

-- Adding data safely: categorise only the new rows
UPDATE transactions
SET category = (
  SELECT r.category
  FROM rules r
  WHERE transactions.description LIKE r.pattern
  ORDER BY r.priority
  LIMIT 1
)
WHERE category IS NULL;

-- Capstone: Alex's questions
-- (If you added the April takeaway in this module, the queries below only look at January to March.)

-- Takeaway
SELECT strftime('%Y-%m', day) AS month, count(*) AS orders, round(-sum(amount), 2) AS spent
FROM transactions
WHERE description = 'QUICKBITE TAKEAWAY' AND day <= '2026-03-31'
GROUP BY month;

-- Subscriptions per year
SELECT description, -amount AS monthly, round(-amount * 12, 2) AS per_year
FROM transactions
WHERE category = 'Subscriptions' AND day BETWEEN '2026-03-01' AND '2026-03-31';

-- Lowest point
SELECT day, description, balance
FROM transactions
WHERE balance IS NOT NULL
ORDER BY balance
LIMIT 1;

-- Pay vs rent
SELECT round(100.0 * (SELECT -sum(amount) FROM transactions WHERE category = 'Rent' AND day <= '2026-03-31')
                    / (SELECT sum(amount) FROM transactions WHERE category = 'Income' AND day <= '2026-03-31'), 1)
       AS rent_percent_of_income;
