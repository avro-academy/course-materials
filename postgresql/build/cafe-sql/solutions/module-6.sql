-- Module 6: Designing tables. Answers to the "Try it" questions.

-- Data types
SELECT '2026-03-14'::date + 30;   -- 2026-04-13: a date plus a number adds days

-- Phone number:            text (it can start with 0, have spaces or a +, and you never add phone numbers up)
-- A shift's start time:    timestamp (a date and a time), or time if it's only ever a time of day
-- Hourly rate:             numeric(5, 2), because it's money
-- Wants emails?            boolean

-- Creating tables
CREATE TABLE suppliers (
  id    integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  name  text NOT NULL UNIQUE,
  phone text,
  email text
);

INSERT INTO suppliers (name, phone, email)
VALUES ('Bean There Roasters', '02 5550 1234', 'orders@beanthere.example.com'),
       ('Fresh Fields Dairy', '02 5550 5678', 'hello@freshfields.example.com');

INSERT INTO suppliers (name) VALUES ('Bean There Roasters');
-- ERROR:  duplicate key value violates unique constraint "suppliers_name_key"

-- Changing tables
ALTER TABLE customers ADD COLUMN wants_emails boolean NOT NULL DEFAULT false;

-- shifts is the table made in the "Creating tables" lesson
ALTER TABLE shifts ADD CONSTRAINT max_12_hours
  CHECK (ends_at - starts_at <= interval '12 hours');
