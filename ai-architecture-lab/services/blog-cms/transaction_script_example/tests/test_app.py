import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture(autouse=True)
def client(tmp_path, monkeypatch):
    # isolate DB per test run
    db_file = tmp_path / "test_posts.db"
    monkeypatch.setenv("DB_PATH", str(db_file))
    # also ensure module-level DB_PATH used by get_db_conn matches
    from importlib import reload
    import app.main as mainmod
    mainmod.DB_PATH = str(db_file)
    reload(mainmod)
    client = TestClient(mainmod.app)
    yield client


def test_create_and_get_post(client):
    payload = {"title": "Hello", "content": "World"}
    r = client.post("/posts", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert data["id"] == 1

    r2 = client.get(f"/posts/{data['id']}")
    assert r2.status_code == 200
    assert r2.json()["title"] == payload["title"]


def test_update_and_delete_post(client):
    payload = {"title": "A", "content": "B"}
    r = client.post("/posts", json=payload)
    pid = r.json()["id"]

    upd = {"title": "X", "content": "Y"}
    r2 = client.put(f"/posts/{pid}", json=upd)
    assert r2.status_code == 200
    assert r2.json()["title"] == "X"

    r3 = client.delete(f"/posts/{pid}")
    assert r3.status_code == 200
    assert r3.json()["deleted"] is True
