"""Shift Swap Board, step 4: saving shifts in a SQLite database.

First time (and whenever schema.sql changes):  flask --app app init-db
Run it:  flask --app app run --debug
"""
import os
import re
import sqlite3
from datetime import date

import click
from flask import Flask, abort, flash, g, redirect, render_template, request, url_for

app = Flask(__name__)
app.config["SECRET_KEY"] = "dev-only-change-me"
app.config["DATABASE"] = os.path.join(app.root_path, "shifts.db")

ROLES = ["Barista", "Kitchen", "Front of house", "Cleaning", "Delivery"]


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row      # rows work like dictionaries
    return g.db


@app.teardown_appcontext
def close_db(error):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    with app.open_resource("schema.sql") as f:
        get_db().executescript(f.read().decode())


@app.cli.command("init-db")
def init_db_command():
    """Delete the database and create empty tables."""
    init_db()
    click.echo("Database ready.")


@app.route("/")
def index():
    shifts = get_db().execute(
        "SELECT * FROM shifts WHERE day >= ? ORDER BY day, start", (date.today().isoformat(),)
    ).fetchall()
    return render_template("index.html", shifts=shifts)


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
        get_db().execute(
            "INSERT INTO shifts (name, day, start, finish, role, note) VALUES (?, ?, ?, ?, ?, ?)",
            (form["name"], form["day"], form["start"], form["finish"], form["role"], form["note"]),
        )
        get_db().commit()
        flash("Shift posted.")
        return redirect(url_for("index"))
    return render_template("new_shift.html", roles=ROLES, form=form)


@app.route("/shifts/<int:shift_id>/delete", methods=["POST"])
def delete_shift(shift_id):
    cur = get_db().execute("DELETE FROM shifts WHERE id = ?", (shift_id,))
    get_db().commit()
    if cur.rowcount == 0:
        abort(404)
    flash("Shift removed.")
    return redirect(url_for("index"))
