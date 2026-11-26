-- The same tables as schema.sql, in PostgreSQL's words.
DROP TABLE IF EXISTS shifts;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    username text UNIQUE NOT NULL,
    password_hash text NOT NULL
);

CREATE TABLE shifts (
    id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    owner_id integer NOT NULL REFERENCES users (id),
    day text NOT NULL,          -- YYYY-MM-DD
    start text NOT NULL,        -- HH:MM
    finish text NOT NULL,
    role text NOT NULL,
    note text NOT NULL DEFAULT '',
    claimed_by integer REFERENCES users (id)
);
