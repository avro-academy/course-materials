"""Shift Swap Board, step 3: forms, checking input and flash messages.

Run it:  flask --app app run --debug
Shifts are kept in a Python list, so they disappear when the server restarts. Step 4 fixes that.
"""
import re
from datetime import date

from flask import Flask, flash, redirect, render_template, request, url_for

app = Flask(__name__)
app.config["SECRET_KEY"] = "dev-only-change-me"   # needed for flash messages (step 6 moves it out of the code)

ROLES = ["Barista", "Kitchen", "Front of house", "Cleaning", "Delivery"]

SHIFTS = [
    {"name": "Sam", "day": "2099-03-14", "start": "07:00", "finish": "12:30", "role": "Barista", "note": "Opening shift"},
]


@app.route("/")
def index():
    return render_template("index.html", shifts=SHIFTS)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/shifts/new", methods=["GET", "POST"])
def new_shift():
    form = {}
    if request.method == "POST":
        form = {k: request.form.get(k, "").strip() for k in ("name", "day", "start", "finish", "role", "note")}
        error = None
        try:
            day = date.fromisoformat(form["day"])
        except ValueError:
            day = None
        if not form["name"]:
            error = "Enter your name."
        elif day is None:
            error = "Choose a date."
        elif day < date.today():
            error = "That date has already passed."
        elif not re.fullmatch(r"\d\d:\d\d", form["start"]) or not re.fullmatch(r"\d\d:\d\d", form["finish"]):
            error = "Enter a start and finish time."
        elif form["finish"] <= form["start"]:
            error = "The finish time must be after the start time."
        elif form["role"] not in ROLES:
            error = "Choose a role."
        if error:
            flash(error)
            return render_template("new_shift.html", roles=ROLES, form=form)
        SHIFTS.append(form)
        flash("Shift posted.")
        return redirect(url_for("index"))
    return render_template("new_shift.html", roles=ROLES, form=form)
