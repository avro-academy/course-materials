"""Shift Swap Board, step 1: your first Flask app.

Run it:  flask --app app run --debug
Then open http://127.0.0.1:5000
"""
from flask import Flask

app = Flask(__name__)


@app.route("/")
def index():
    return "<h1>Shift Swap Board</h1><p>Coming soon!</p>"


@app.route("/about")
def about():
    return "<p>Post shifts you can't work. Take shifts you can.</p>"


@app.route("/hello/<name>")
def hello(name):
    return f"<p>Hi {name}, welcome to Shift Swap!</p>"


@app.route("/shifts/<int:shift_id>")
def show_shift(shift_id):
    return f"Shift number {shift_id}"     # /shifts/7 works, /shifts/abc gives 404
