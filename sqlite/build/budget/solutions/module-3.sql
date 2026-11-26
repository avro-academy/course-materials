-- Module 3: How SQLite is different. Answers to the "Try it" questions.

-- SQLite's flexible types
SELECT typeof(id), typeof(day), typeof(description), typeof(amount), typeof(balance), typeof(category)
FROM transactions
LIMIT 1;
-- integer, text, text, real, real, and text (or null before Module 4 fills in categories)

SELECT sum(CASE WHEN amount > 0 THEN CAST(round(amount * 100) AS INTEGER) ELSE 0 END) AS cents_in,
       sum(CASE WHEN amount < 0 THEN CAST(round(-amount * 100) AS INTEGER) ELSE 0 END) AS cents_out
FROM transactions;
-- 549885 in and 582878 out: exact, with no tiny errors

-- Dates and times
SELECT strftime('%Y-%m', day) AS month, round(-sum(amount), 2) AS money_out
FROM transactions
WHERE amount < 0
GROUP BY month;

SELECT date('2026-04-01', 'weekday 4') AS next_thursday;   -- 2026-04-02
-- Paydays are every 14 days from 26 March, so the next one is 9 April:
SELECT date('2026-03-26', '+14 days') AS next_payday;

-- Keys and the foreign keys switch
PRAGMA foreign_keys = ON;
INSERT INTO rules (pattern, category) VALUES ('%AIRLINE%', 'Holidays');
-- Runtime error: FOREIGN KEY constraint failed

-- In a new session (.quit, then sqlite3 budget.db again):
PRAGMA foreign_keys;   -- 0: it's off again
