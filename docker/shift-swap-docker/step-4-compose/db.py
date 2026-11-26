"""Shift Swap's database connection.

With DATABASE_URL set (as in compose.yaml) the app uses PostgreSQL; without it,
the SQLite file in DATABASE, as in Modules 2 to 4. The tests use SQLite.
"""
import os
import sqlite3

from flask import current_app

try:
    import psycopg
    from psycopg.rows import dict_row
except ImportError:  # psycopg isn't needed for SQLite
    psycopg = None

# The error for "that username is already taken", from either database
IntegrityError = (sqlite3.IntegrityError,) + ((psycopg.IntegrityError,) if psycopg else ())


class PostgresConnection:
    """Makes a PostgreSQL connection work like the sqlite3 one the app was written for."""

    def __init__(self, url):
        self.conn = psycopg.connect(url, row_factory=dict_row)  # rows work like dictionaries

    def execute(self, sql, params=()):
        return self.conn.execute(sql.replace("?", "%s"), params)  # PostgreSQL writes parameters as %s

    def executescript(self, script):
        self.conn.execute(script)
        self.conn.commit()

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()


def using_postgres():
    return bool(os.environ.get("DATABASE_URL"))


def connect():
    if using_postgres():
        return PostgresConnection(os.environ["DATABASE_URL"])
    conn = sqlite3.connect(current_app.config["DATABASE"])
    conn.row_factory = sqlite3.Row
    return conn


def schema_file():
    return "schema-postgres.sql" if using_postgres() else "schema.sql"
