"""Shift Swap Board, step 6: the finished app (security, JSON API, JavaScript and tests)."""
import os
import re
import secrets
import sqlite3
from datetime import date
from functools import wraps

import click
from flask import (Flask, abort, flash, g, jsonify, redirect, render_template,
                   request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-only-change-me")
app.config["DATABASE"] = os.environ.get("DATABASE", os.path.join(app.root_path, "shifts.db"))

ROLES = ["Barista", "Kitchen", "Front of house", "Cleaning", "Delivery"]


# ---------- Database ----------

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


# ---------- Security helpers ----------

def csrf_token():
    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_hex(16)
    return session["csrf_token"]


app.jinja_env.globals["csrf_token"] = csrf_token


@app.before_request
def check_csrf():
    if request.method == "POST":
        sent = request.form.get("csrf_token") or request.headers.get("X-CSRF-Token")
        if not sent or not secrets.compare_digest(sent, session.get("csrf_token", "")):
            abort(400, "Missing or wrong security token. Go back, refresh the page and try again.")


def safe_next(target):
    """Only follow ?next= links that stay on this site."""
    return target if target and target.startswith("/") and not target.startswith("//") else url_for("index")


# ---------- Users ----------

@app.before_request
def load_user():
    user_id = session.get("user_id")
    g.user = None
    if user_id is not None:
        g.user = get_db().execute("SELECT id, username FROM users WHERE id = ?", (user_id,)).fetchone()


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if g.user is None:
            if request.path.startswith("/api/"):
                return jsonify(error="Please log in first."), 401
            flash("Please log in first.")
            return redirect(url_for("login", next=request.path))
        return view(*args, **kwargs)
    return wrapped


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        error = None
        if not re.fullmatch(r"[A-Za-z0-9_]{3,20}", username):
            error = "Usernames are 3–20 letters, numbers or underscores."
        elif len(password) < 8:
            error = "Passwords need at least 8 characters."
        if error is None:
            try:
                get_db().execute("INSERT INTO users (username, password_hash) VALUES (?, ?)",
                                 (username, generate_password_hash(password)))
                get_db().commit()
            except sqlite3.IntegrityError:
                error = f"{username} is already taken."
            else:
                flash("Account created — please log in.")
                return redirect(url_for("login"))
        flash(error)
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        user = get_db().execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        if user is None or not check_password_hash(user["password_hash"], request.form.get("password", "")):
            flash("Wrong username or password.")
        else:
            session.clear()
            session["user_id"] = user["id"]
            flash(f"Welcome back, {user['username']}!")
            return redirect(safe_next(request.args.get("next")))
    return render_template("login.html")


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    flash("You're logged out.")
    return redirect(url_for("index"))


# ---------- Shifts ----------

def open_shifts():
    return get_db().execute(
        """SELECT shifts.*, users.username AS owner_name FROM shifts
           JOIN users ON users.id = shifts.owner_id
           WHERE shifts.claimed_by IS NULL AND shifts.day >= ?
           ORDER BY shifts.day, shifts.start""",
        (date.today().isoformat(),),
    ).fetchall()


def check_shift_form(form):
    """Returns an error message, or None if the form is fine."""
    try:
        day = date.fromisoformat(form["day"])
    except ValueError:
        day = None
    if day is None:
        return "Choose a date."
    if day < date.today():
        return "That date has already passed."
    if not re.fullmatch(r"\d\d:\d\d", form["start"]) or not re.fullmatch(r"\d\d:\d\d", form["finish"]):
        return "Enter a start and finish time."
    if form["finish"] <= form["start"]:
        return "The finish time must be after the start time."
    if form["role"] not in ROLES:
        return "Choose a role."
    if len(form["note"]) > 200:
        return "Keep the note under 200 characters."
    return None


def claim(shift_id):
    """Give the shift to the logged-in user. Returns an error message, or None if it worked."""
    shift = get_db().execute("SELECT * FROM shifts WHERE id = ?", (shift_id,)).fetchone()
    if shift is None:
        return "That shift doesn't exist."
    if shift["owner_id"] == g.user["id"]:
        return "You can't take your own shift."
    # Only succeeds if nobody else claimed it first.
    cur = get_db().execute("UPDATE shifts SET claimed_by = ? WHERE id = ? AND claimed_by IS NULL",
                           (g.user["id"], shift_id))
    get_db().commit()
    return None if cur.rowcount == 1 else "Sorry, someone else just took that shift."


@app.route("/")
def index():
    return render_template("index.html", shifts=open_shifts())


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/shifts/new", methods=["GET", "POST"])
@login_required
def new_shift():
    form = {}
    if request.method == "POST":
        form = {k: request.form.get(k, "").strip() for k in ("day", "start", "finish", "role", "note")}
        error = check_shift_form(form)
        if error:
            flash(error)
            return render_template("new_shift.html", roles=ROLES, form=form)
        get_db().execute(
            "INSERT INTO shifts (owner_id, day, start, finish, role, note) VALUES (?, ?, ?, ?, ?, ?)",
            (g.user["id"], form["day"], form["start"], form["finish"], form["role"], form["note"]),
        )
        get_db().commit()
        flash("Shift posted.")
        return redirect(url_for("index"))
    return render_template("new_shift.html", roles=ROLES, form=form)


@app.route("/shifts/<int:shift_id>/claim", methods=["POST"])
@login_required
def claim_shift(shift_id):
    error = claim(shift_id)
    flash(error or "It's yours! The shift is now in My shifts.")
    return redirect(url_for("index") if error else url_for("my_shifts"))


@app.route("/shifts/<int:shift_id>/delete", methods=["POST"])
@login_required
def delete_shift(shift_id):
    shift = get_db().execute("SELECT * FROM shifts WHERE id = ?", (shift_id,)).fetchone()
    if shift is None:
        abort(404)
    if shift["owner_id"] != g.user["id"]:
        abort(403)
    get_db().execute("DELETE FROM shifts WHERE id = ?", (shift_id,))
    get_db().commit()
    flash("Shift removed.")
    return redirect(url_for("my_shifts"))


@app.route("/my-shifts")
@login_required
def my_shifts():
    posted = get_db().execute(
        """SELECT shifts.*, taker.username AS taker_name FROM shifts
           LEFT JOIN users AS taker ON taker.id = shifts.claimed_by
           WHERE shifts.owner_id = ? ORDER BY shifts.day, shifts.start""",
        (g.user["id"],),
    ).fetchall()
    covering = get_db().execute(
        """SELECT shifts.*, owner.username AS owner_name FROM shifts
           JOIN users AS owner ON owner.id = shifts.owner_id
           WHERE shifts.claimed_by = ? ORDER BY shifts.day, shifts.start""",
        (g.user["id"],),
    ).fetchall()
    return render_template("my_shifts.html", posted=posted, covering=covering)


# ---------- JSON API ----------

def shift_json(row):
    return {"id": row["id"], "day": row["day"], "start": row["start"], "finish": row["finish"],
            "role": row["role"], "note": row["note"], "posted_by": row["owner_name"]}


@app.route("/api/shifts")
def api_shifts():
    return jsonify([shift_json(s) for s in open_shifts()])


@app.route("/api/shifts/<int:shift_id>/claim", methods=["POST"])
@login_required
def api_claim(shift_id):
    error = claim(shift_id)
    if error:
        return jsonify(error=error), 409
    return jsonify(ok=True, message="It's yours! The shift is now in My shifts.")


# ---------- Template helpers ----------

@app.template_filter("nice_date")
def nice_date(value):
    """2026-03-14 -> Sat 14 Mar"""
    try:
        return date.fromisoformat(value).strftime("%a %d %b").replace(" 0", " ")
    except ValueError:
        return value


@app.errorhandler(403)
def forbidden(error):
    return render_template("error.html", title="Not allowed", message="Only the person who posted that shift can do that."), 403


@app.errorhandler(404)
def not_found(error):
    return render_template("error.html", title="Not found", message="We couldn't find that page or shift."), 404
