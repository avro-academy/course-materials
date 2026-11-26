"""Add some bookings for the coming Saturday, so that 10:00 and 10:30 are full.

    python seed.py
"""
import datetime as dt

import bookings


def coming_saturday():
    days = (5 - bookings.today().weekday()) % 7 or 7
    return (bookings.today() + dt.timedelta(days=days)).isoformat()


def seed():
    day = coming_saturday()
    with bookings.connect() as conn:
        conn.execute("DELETE FROM bookings WHERE day = ? AND name LIKE 'Seed %'", (day,))
    for time, groups in {"09:00": [4, 2], "10:00": [6, 6, 4, 4], "10:30": [8, 6, 6], "12:00": [4]}.items():
        for i, people in enumerate(groups, 1):
            bookings.add_booking(f"Seed {time} #{i}", day, time, people)
    return day


if __name__ == "__main__":
    day = seed()
    print(f"Added bookings for Saturday {day} - 10:00 and 10:30 are now full.")
