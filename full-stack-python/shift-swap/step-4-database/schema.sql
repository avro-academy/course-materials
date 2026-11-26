DROP TABLE IF EXISTS shifts;

CREATE TABLE shifts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    day TEXT NOT NULL,          -- YYYY-MM-DD
    start TEXT NOT NULL,        -- HH:MM
    finish TEXT NOT NULL,
    role TEXT NOT NULL,
    note TEXT NOT NULL DEFAULT ''
);
