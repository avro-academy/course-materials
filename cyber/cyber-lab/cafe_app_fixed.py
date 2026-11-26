"""Corner Café staff orders app — the fixed version (Cyber Security, Module 5).

    CAFE_SECRET_KEY=... python3 cafe_app.py
"""
import hashlib
import html
import os
import sqlite3

from flask import Flask, request

app = Flask(__name__)
SECRET_KEY = os.environ["CAFE_SECRET_KEY"]   # fixed: the secret comes from outside the code
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


@app.after_request
def security_headers(response):
    # fixed: a second layer — browsers only run scripts from this site, and won't show it inside other sites
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    return response


@app.post("/login")
def login():
    username = request.form["username"]
    password_hash = hashlib.sha256(request.form["password"].encode()).hexdigest()
    # fixed: ? placeholders — the database treats what people type as data, never as SQL
    query = "SELECT username, role FROM users WHERE username = ? AND password_hash = ?"
    user = db().execute(query, (username, password_hash)).fetchone()
    if user:
        return f"Welcome, {html.escape(user['username'])}! You're logged in as {user['role']}.\n"
    return "Wrong username or password.\n", 401


@app.get("/reviews")
def reviews():
    rows = db().execute("SELECT name, text FROM reviews").fetchall()
    # fixed: escape what people typed, so <script> shows as text instead of running
    items = "".join(f"<li><b>{html.escape(r['name'])}</b>: {html.escape(r['text'])}</li>" for r in rows)
    return f"<!doctype html><title>Reviews</title><h1>What customers say</h1><ul>{items}</ul>\n"


@app.post("/reviews")
def add_review():
    name, text = request.form.get("name", "").strip(), request.form.get("text", "").strip()
    if not name or not text or len(name) > 50 or len(text) > 500:   # fixed: limit what people can send
        return "Please give a name (up to 50 characters) and a review (up to 500).\n", 400
    with db() as conn:
        conn.execute("INSERT INTO reviews (name, text) VALUES (?, ?)", (name, text))
    return "Thanks for your review!\n"


if __name__ == "__main__":
    setup()
    app.run(host="0.0.0.0", port=5000)
