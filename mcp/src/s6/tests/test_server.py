"""Tests for the café's MCP server, through a real MCP client session connected in memory.
No separate program and no Ollama needed (search_handbook isn't called here).

python -m pytest -q
"""
import datetime as dt

import pytest
from mcp.shared.memory import create_connected_server_and_client_session

import bookings
import server

DAY = (dt.date.today() + dt.timedelta(days=7)).isoformat()


@pytest.fixture(autouse=True)
def fresh_db(tmp_path, monkeypatch):
    """Every test gets its own empty bookings database."""
    monkeypatch.setattr(bookings, "DB", str(tmp_path / "test.db"))


@pytest.fixture
def anyio_backend():
    return "asyncio"


def session():
    return create_connected_server_and_client_session(server.mcp._mcp_server)


@pytest.mark.anyio
async def test_the_server_lists_its_tools_resources_and_prompts():
    async with session() as s:
        assert {t.name for t in (await s.list_tools()).tools} == {"booking_times", "request_booking", "search_handbook"}
        assert {str(r.uri) for r in (await s.list_resources()).resources} == {"cafe://menu", "cafe://hours"}
        assert [t.uriTemplate for t in (await s.list_resource_templates()).resourceTemplates] == ["cafe://bookings/{date}"]
        assert {p.name for p in (await s.list_prompts()).prompts} == {"reply_to_customer", "new_staff_welcome"}


@pytest.mark.anyio
async def test_tool_schemas_and_annotations():
    async with session() as s:
        tools = {t.name: t for t in (await s.list_tools()).tools}
    check = tools["booking_times"]
    assert check.inputSchema["required"] == ["date", "people"]
    assert check.inputSchema["properties"]["people"]["type"] == "integer"
    assert check.annotations.readOnlyHint is True
    request = tools["request_booking"].annotations
    assert request.readOnlyHint is False and request.destructiveHint is False and request.idempotentHint is False


@pytest.mark.anyio
async def test_booking_times_says_when_a_time_is_full():
    for people in (8, 8, 4):
        bookings.add_booking("Guest", DAY, "10:00", people)
    async with session() as s:
        full = await s.call_tool("booking_times", {"date": DAY, "people": 2, "time": "10:00"})
        free = await s.call_tool("booking_times", {"date": DAY, "people": 2, "time": "09:30"})
        bad = await s.call_tool("booking_times", {"date": DAY, "people": 40})
    assert full.content[0].text.startswith("No: 10:00") and free.content[0].text.startswith("Yes: 09:30")
    assert "1 to 8 people" in bad.content[0].text


@pytest.mark.anyio
async def test_request_booking_waits_for_staff():
    async with session() as s:
        sent = await s.call_tool("request_booking", {"name": "  Jo   Smith  ", "date": DAY, "time": "09:00", "people": 3})
        past = await s.call_tool("request_booking", {"name": "Jo", "date": "2020-01-01", "time": "09:00", "people": 3})
    assert sent.content[0].text.startswith("Request sent: Jo Smith, 3 people")
    assert "in the past" in past.content[0].text
    waiting = bookings.waiting_requests()
    assert [(r["name"], r["day"], r["time"], r["people"], r["thread_id"]) for r in waiting] == [("Jo Smith", DAY, "09:00", 3, "mcp")]
    assert bookings.bookings_on(DAY) == []  # nothing is booked until staff approve it


@pytest.mark.anyio
async def test_resources_and_templates():
    bookings.add_booking("Guest", DAY, "11:00", 6)
    async with session() as s:
        menu = await s.read_resource("cafe://menu")
        day = await s.read_resource(f"cafe://bookings/{DAY}")
        past = await s.read_resource("cafe://bookings/2020-01-01")
    assert menu.contents[0].text.startswith("# Menu and prices")
    assert "11:00   6 of 20 seats booked" in day.contents[0].text
    assert "in the past" in past.contents[0].text


@pytest.mark.anyio
async def test_prompts():
    async with session() as s:
        reply = await s.get_prompt("reply_to_customer", {"message": "Are you open on Anzac Day?"})
        welcome = await s.get_prompt("new_staff_welcome", {"name": "Mia"})
    assert reply.messages[0].content.text.endswith("Customer message:\nAre you open on Anzac Day?")
    assert "Mia, who is starting at Corner Café as a barista" in welcome.messages[0].content.text


@pytest.mark.anyio
async def test_the_token_check(monkeypatch):
    monkeypatch.setattr(server, "TOKEN", "a-long-random-secret")
    verifier = server.StaffToken()
    assert (await verifier.verify_token("a-long-random-secret")).client_id == "cafe-staff"
    assert await verifier.verify_token("wrong-token") is None
    monkeypatch.setattr(server, "TOKEN", "")
    assert await verifier.verify_token("") is None  # no token set: nothing gets in
    with pytest.raises(SystemExit):
        server.make_server(http=True)
