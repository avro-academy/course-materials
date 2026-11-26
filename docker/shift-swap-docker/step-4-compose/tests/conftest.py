import os
import secrets
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import app as flask_app, init_db  # noqa: E402

FUTURE_DAY = "2099-03-14"


@pytest.fixture
def app(tmp_path, monkeypatch):
    monkeypatch.delenv("DATABASE_URL", raising=False)  # the tests always use SQLite
    flask_app.config.update(TESTING=True, DATABASE=str(tmp_path / "test.db"))
    with flask_app.app_context():
        init_db()
    yield flask_app


@pytest.fixture
def client(app):
    return app.test_client()


class Helper:
    """Short-cuts so each test reads like a story."""

    def __init__(self, client):
        self.client = client

    def token(self):
        with self.client.session_transaction() as s:
            if "csrf_token" not in s:
                s["csrf_token"] = secrets.token_hex(16)
            return s["csrf_token"]

    def register(self, username="sam", password="correct horse"):
        return self.client.post("/register", data={"username": username, "password": password, "csrf_token": self.token()},
                                follow_redirects=True)

    def login(self, username="sam", password="correct horse"):
        return self.client.post("/login", data={"username": username, "password": password, "csrf_token": self.token()},
                                follow_redirects=True)

    def logout(self):
        return self.client.post("/logout", data={"csrf_token": self.token()}, follow_redirects=True)

    def post_shift(self, day=FUTURE_DAY, start="07:00", finish="12:30", role="Barista", note="Opening shift"):
        return self.client.post("/shifts/new", data={"day": day, "start": start, "finish": finish, "role": role,
                                                     "note": note, "csrf_token": self.token()}, follow_redirects=True)


@pytest.fixture
def helper(client):
    return Helper(client)
