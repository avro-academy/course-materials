"""Corner Café staff orders app — PRACTICE ONLY. It has security bugs on purpose (Cyber Security, Module 5).

    python3 cafe_app.py        (lab-setup.sh starts it for you on port 5000)
"""
import hashlib
import sqlite3

from flask import Flask, request

app = Flask(__name__)
SECRET_KEY = "cafe-super-secret-2026"   # bug: a secret written in the code
app.config.from_object(__name__)   # Flask reads its settings from the capitals above
DB = "cafe.db"

STAFF = [("admin", "Kettle-Harbour-Violin-77", "manager"), ("sam", "flat-white-every-day", "staff"),
         ("jo", "Coffee2026", "staff")]


def db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


def setup():
    """Make the database the first time the app runs: the staff accounts and one review."""
    with db() as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password_hash TEXT, role TEXT)")
        conn.execute("CREATE TABLE IF NOT EXISTS reviews (id INTEGER PRIMARY KEY, name TEXT, text TEXT)")
        if not conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]:
            for username, password, role in STAFF:
                conn.execute("INSERT INTO users VALUES (?, ?, ?)",
                             (username, hashlib.sha256(password.encode()).hexdigest(), role))
            conn.execute("INSERT INTO reviews (name, text) VALUES (?, ?)", ("Jo", "Best flat white in town!"))


@app.post("/login")
def login():
    username = request.form["username"]
    password_hash = hashlib.sha256(request.form["password"].encode()).hexdigest()
    # bug: what the person typed is pasted straight into the SQL
    query = f"SELECT username, role FROM users WHERE username = '{username}' AND password_hash = '{password_hash}'"
    user = db().execute(query).fetchone()
    if user:
        return f"Welcome, {user['username']}! You're logged in as {user['role']}.\n"
    return "Wrong username or password.\n", 401


@app.get("/reviews")
def reviews():
    rows = db().execute("SELECT name, text FROM reviews").fetchall()
    # bug: reviews go into the page as HTML, exactly as people typed them
    items = "".join(f"<li><b>{r['name']}</b>: {r['text']}</li>" for r in rows)
    return f"<!doctype html><title>Reviews</title><h1>What customers say</h1><ul>{items}</ul>\n"


@app.post("/reviews")
def add_review():
    with db() as conn:
        conn.execute("INSERT INTO reviews (name, text) VALUES (?, ?)", (request.form["name"], request.form["text"]))
    return "Thanks for your review!\n"


if __name__ == "__main__":
    setup()
    app.run(host="0.0.0.0", port=5000)   # bug: open to the whole network
