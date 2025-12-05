import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client(tmp_path, monkeypatch):
    # Point repository at a temp SQLite file and reload api to pick it up.
    db_file = tmp_path / "test_conversations.db"
    monkeypatch.setenv("DB_PATH", str(db_file))
    from importlib import reload, import_module

    api = import_module("app.api")
    reload(api)
    return TestClient(api.app)


def test_create_add_message_and_get(client):
    # create conversation
    r = client.post("/conversations", json={"title": "Chat"})
    assert r.status_code == 200
    conv = r.json()
    cid = conv["id"]
    assert conv["messages"] == []

    # add a message
    r2 = client.post(f"/conversations/{cid}/messages", json={"sender": "alice", "text": "hi"})
    assert r2.status_code == 200
    data = r2.json()
    assert data["id"] == cid
    assert len(data["messages"]) == 1
    assert data["messages"][0]["text"] == "hi"

    # fetch and verify
    r3 = client.get(f"/conversations/{cid}")
    assert r3.status_code == 200
    assert r3.json()["messages"][0]["sender"] == "alice"


def test_close_blocks_new_messages(client):
    r = client.post("/conversations", json={"title": "Closable"})
    cid = r.json()["id"]

    # close
    rc = client.post(f"/conversations/{cid}/close")
    assert rc.status_code == 200
    assert rc.json()["closed"] is True

    # adding after close should 400
    r2 = client.post(f"/conversations/{cid}/messages", json={"sender": "bob", "text": "late"})
    assert r2.status_code == 400
