-- Module 1: Meet PostgreSQL. Answers to the "Try it" questions.
-- These are psql commands (they start with a backslash), so run them in psql.

-- 1. Describe the orders table.
\d orders
-- Columns: id, ordered_at, staff_id, customer_id, payment.
-- staff_id must be a real staff member and customer_id a real customer (foreign keys),
-- customer_id can be empty (NULL), and payment must be 'Card' or 'Cash'.

-- 2. List all the databases on your server.
\l
-- You'll see cafe, postgres and two called template0 and template1,
-- which PostgreSQL uses as patterns for new databases.
