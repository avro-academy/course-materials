-- Module 1: Meet SQLite. Answers to the "Try it" questions.
-- Start with:  sqlite3 budget.db

CREATE TABLE goals (id INTEGER PRIMARY KEY, goal TEXT);
INSERT INTO goals (goal) VALUES ('Save $500 for a new laptop'), ('Keep $1,000 for emergencies');
SELECT * FROM goals;

.schema goals
DROP TABLE goals;
