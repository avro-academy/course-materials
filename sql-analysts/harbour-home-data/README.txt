Harbour & Home dataset (made-up data) for Avro Academy's SQL for Data Analysts course

harbour_home.sqlite  The database. Open it in DB Browser for SQLite (free) or any SQLite tool.
harbour_home.sql     The same data as SQL statements. Run it in any SQLite tool to rebuild the database.
csv/                 One CSV per table, for Excel or Google Sheets.

Tables
  channels     6 rows     marketing channels customers came from
  customers    1,512 rows  sign-ups (state is deliberately messy, some cities are missing)
  products     43 rows    list_price and unit_cost in dollars
  orders       4,633 rows  1 Jan to 31 Dec 2025, status, discount code, shipping fee
  order_items  8,109 rows  one row per product in an order
  returns      407 rows   returned items with a reason

It is the same database the online SQL playground uses, so every lesson result matches.
