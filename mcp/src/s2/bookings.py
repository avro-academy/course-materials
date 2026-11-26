"""Corner Café's table bookings, and booking requests waiting for staff, in a small SQLite database (bookings.db).
The same booking system as Café Helper in the LangGraph course.

The café has 20 seats inside for bookings, and takes bookings every half hour from 08:00 to 13:00.
Everything a tool sends is checked here, in code: an AI app's arguments are never trusted.
"""
import datetime as dt
import os
import re
import sqlite3

DB = os.environ.get("BOOKINGS_DB", os.path.join(os.path.dirname(os.path.abspath(__file__)), "bookings.db"))
SEATS_PER_TIME = 20            # seats for bookings at any one time
MAX_PEOPLE = 8                 # bigger groups phone the café
DAYS_AHEAD = 60                # how far ahead you can book
TIMES = [f"{h:02d}:{m:02d}" for h in range(8, 14) for m in (0, 30)][:-1]   # 08:00 ... 13:00
CLOSED = {"12-25", "12-26", "01-01"}   # Christmas Day, Boxing Day, New Year's Day (MM-DD)

SCHEMA = """
CREATE TABLE IF NOT EXISTS bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    day TEXT NOT NULL,            -- YYYY-MM-DD
    time TEXT NOT NULL,           -- HH:MM
    people INTEGER NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tool_call_id TEXT UNIQUE NOT NULL,   -- the same request is only stored once
    thread_id TEXT NOT NULL,             -- where it came from: a conversation, or "mcp"
    name TEXT NOT NULL,
    day TEXT NOT NULL,
    time TEXT NOT NULL,
    people INTEGER NOT NULL,
    status TEXT NOT NULL DEFAULT 'waiting',   -- waiting, approved or declined
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
"""


def connect():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA)
    return conn


def today():
    return dt.date.today()


def problem_with(date, people, time=None):
    """What's wrong with a booking request, as a message the model can pass on, or None if it's fine."""
    try:
        day = dt.date.fromisoformat(str(date))
    except ValueError:
        return f"'{date}' isn't a date. Use YYYY-MM-DD, like {today().isoformat()}."
    if day < today():
        return f"{date} is in the past."
    if day > today() + dt.timedelta(days=DAYS_AHEAD):
        return f"Online bookings are only for the next {DAYS_AHEAD} days."
    if day.strftime("%m-%d") in CLOSED:
        return f"The café is closed on {date}."
    if not isinstance(people, int) or not 1 <= people <= MAX_PEOPLE:
        return f"Online bookings are for 1 to {MAX_PEOPLE} people. For bigger groups, phone (02) 5550 0000."
    if time is not None:
        if not re.fullmatch(r"\d\d:\d\d", str(time)) or time not in TIMES:
            return f"{time} isn't a booking time. Bookings are every half hour from 08:00 to 13:00."
        if day == today() and time <= dt.datetime.now().strftime("%H:%M"):
            return f"{time} today has already gone."
    return None


def seats_taken(date):
    """Seats booked at each booking time on date: {"08:00": 0, "08:30": 4, ...}."""
    with connect() as conn:
        rows = dict(conn.execute("SELECT time, SUM(people) FROM bookings WHERE day = ? GROUP BY time", (date,)).fetchall())
    return {t: rows.get(t, 0) for t in TIMES}


def free_times(date, people):
    """The booking times on date that still have room for this many people."""
    now = dt.datetime.now().strftime("%H:%M") if date == today().isoformat() else ""
    return [t for t, taken in seats_taken(date).items() if t > now and taken + people <= SEATS_PER_TIME]


def add_booking(name, date, time, people):
    with connect() as conn:
        cur = conn.execute("INSERT INTO bookings (name, day, time, people) VALUES (?, ?, ?, ?)", (name, date, time, people))
        return cur.lastrowid


def bookings_on(date):
    with connect() as conn:
        return [dict(r) for r in conn.execute("SELECT * FROM bookings WHERE day = ? ORDER BY time, id", (date,))]


# ---- Booking requests: an AI app asks, staff answer ----

def add_request(request_id, source, name, date, time, people):
    """Store a booking request for staff. Safe to repeat: the same request_id is only stored once."""
    with connect() as conn:
        conn.execute("INSERT OR IGNORE INTO requests (tool_call_id, thread_id, name, day, time, people) "
                     "VALUES (?, ?, ?, ?, ?, ?)", (request_id, source, name, date, time, people))


def set_request_status(request_id, status):
    with connect() as conn:
        conn.execute("UPDATE requests SET status = ? WHERE id = ?", (status, request_id))


def waiting_requests():
    with connect() as conn:
        return [dict(r) for r in conn.execute("SELECT * FROM requests WHERE status = 'waiting' ORDER BY id")]
