"""Shift Swap Board, step 2: templates and static files.

Run it:  flask --app app run --debug
"""
from flask import Flask, render_template

app = Flask(__name__)

SHIFTS = [
    {"day": "Sat 14 Mar", "start": "07:00", "finish": "12:30", "role": "Barista", "posted_by": "sam"},
    {"day": "Sun 15 Mar", "start": "11:00", "finish": "15:00", "role": "Kitchen", "posted_by": "priya"},
]


@app.route("/")
def index():
    return render_template("index.html", shifts=SHIFTS)


@app.route("/about")
def about():
    return render_template("about.html")
