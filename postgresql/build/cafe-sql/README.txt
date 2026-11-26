CORNER CAFÉ DATABASE: starter files
Avro Academy · PostgreSQL Foundations: Run the Corner Café Database

  cafe.sql        builds the café database: 6 tables and March 2026's sales
  solutions/      answers to every "Try it" question, one file per module,
                  plus the capstone report (module-8.sql)

LOAD IT (Module 1 shows each step)
  In psql:
    CREATE DATABASE cafe;
    \c cafe
    \i cafe.sql

  Give the full path if psql wasn't started in this folder. On Windows use
  forward slashes and quotes:  \i 'C:/Users/you/Downloads/cafe-sql/cafe.sql'

  Run \i cafe.sql again any time to put everything back to how it started.

THE TABLES
  categories    Coffee, Tea, Drinks, Food
  menu_items    15 items, with prices
  staff         6 people who work there
  customers     25 loyalty-card members
  orders        1,492 orders in March 2026
  order_items   what was in each order, and how many

Corner Café and everyone in it are made up. Any likeness to a real café or
person is a coincidence.
