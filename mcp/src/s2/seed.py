"""Fill this coming Saturday with some bookings, so there's something to see: 10:00 and 10:30 full, 11:00 busy.

python seed.py
"""
import datetime

import bookings

today = datetime.date.today()
saturday = (today + datetime.timedelta(days=(5 - today.weekday()) % 7 or 7)).isoformat()

with bookings.connect() as conn:
    conn.execute("DELETE FROM bookings WHERE day = ?", (saturday,))  # run it twice, get the same bookings
for time, groups in {"10:00": [8, 6, 4, 2], "10:30": [8, 8, 4], "11:00": [6, 4, 2]}.items():
    for n, people in enumerate(groups, start=1):
        bookings.add_booking(f"Guest {n}", saturday, time, people)
print(f"Added bookings for Saturday {saturday} - 10:00 and 10:30 are now full.")
