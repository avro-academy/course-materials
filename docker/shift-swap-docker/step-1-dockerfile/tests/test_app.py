"""Tests for the Shift Swap Board. Run them with: python -m pytest"""


def test_board_loads_when_empty(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"No open shifts" in response.data


def test_register_and_login(helper):
    assert b"Account created" in helper.register().data
    assert b"Welcome back, sam!" in helper.login().data


def test_duplicate_username_refused(helper):
    helper.register()
    assert b"sam is already taken" in helper.register().data


def test_short_password_refused(helper):
    assert b"at least 8 characters" in helper.register(password="short").data


def test_wrong_password(helper):
    helper.register()
    assert b"Wrong username or password" in helper.login(password="not my password").data


def test_sql_injection_attempt_is_harmless(helper):
    helper.register()
    response = helper.login(username="sam' OR '1'='1", password="anything")
    assert b"Wrong username or password" in response.data


def test_passwords_are_hashed(helper, app):
    helper.register(password="correct horse")
    with app.app_context():
        from app import get_db
        stored = get_db().execute("SELECT password_hash FROM users").fetchone()[0]
    assert "correct horse" not in stored


def test_posting_needs_login(client):
    response = client.get("/shifts/new")
    assert response.status_code == 302
    assert "/login?next=/shifts/new" in response.headers["Location"]


def test_post_shift_shows_on_board(helper, client):
    helper.register(); helper.login()
    assert b"Shift posted" in helper.post_shift().data
    html = client.get("/").get_data(as_text=True)
    assert "Barista" in html and "Posted by sam" in html


def test_finish_must_be_after_start(helper):
    helper.register(); helper.login()
    assert b"finish time must be after the start time" in helper.post_shift(start="12:00", finish="09:00").data


def test_past_dates_refused(helper):
    helper.register(); helper.login()
    assert b"already passed" in helper.post_shift(day="2020-01-01").data


def test_notes_are_escaped(helper, client):
    helper.register(); helper.login()
    helper.post_shift(note="<script>alert(1)</script>")
    html = client.get("/").get_data(as_text=True)
    assert "<script>alert(1)</script>" not in html
    assert "&lt;script&gt;" in html


def test_post_without_csrf_token_is_refused(helper, client):
    helper.register(); helper.login()
    response = client.post("/shifts/new", data={"day": "2099-03-14", "start": "07:00", "finish": "12:30", "role": "Barista"})
    assert response.status_code == 400


def test_only_owner_can_delete(helper, client):
    helper.register("sam"); helper.login("sam"); helper.post_shift(); helper.logout()
    helper.register("ali"); helper.login("ali")
    shift_id = client.get("/api/shifts").get_json()[0]["id"]
    response = client.post(f"/shifts/{shift_id}/delete", data={"csrf_token": helper.token()})
    assert response.status_code == 403


def test_take_a_shift_and_it_leaves_the_board(helper, client):
    helper.register("sam"); helper.login("sam"); helper.post_shift(); helper.logout()
    helper.register("ali"); helper.login("ali")
    shift_id = client.get("/api/shifts").get_json()[0]["id"]
    response = client.post(f"/api/shifts/{shift_id}/claim", headers={"X-CSRF-Token": helper.token()})
    assert response.status_code == 200
    assert client.get("/api/shifts").get_json() == []
    assert b"For sam" in client.get("/my-shifts").data


def test_same_shift_cannot_be_taken_twice(helper, client):
    helper.register("sam"); helper.login("sam"); helper.post_shift(); helper.logout()
    helper.register("ali"); helper.login("ali")
    shift_id = client.get("/api/shifts").get_json()[0]["id"]
    client.post(f"/api/shifts/{shift_id}/claim", headers={"X-CSRF-Token": helper.token()})
    helper.logout()
    helper.register("kim"); helper.login("kim")
    response = client.post(f"/api/shifts/{shift_id}/claim", headers={"X-CSRF-Token": helper.token()})
    assert response.status_code == 409
    assert "someone else" in response.get_json()["error"]


def test_safe_next_ignores_other_sites(helper, client):
    helper.register()
    response = client.post("/login?next=https://evil.example", data={"username": "sam", "password": "correct horse",
                                                                    "csrf_token": helper.token()})
    assert response.headers["Location"] == "/"
