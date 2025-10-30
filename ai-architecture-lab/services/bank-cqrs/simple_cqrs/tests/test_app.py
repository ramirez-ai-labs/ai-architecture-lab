import pytest
from fastapi.testclient import TestClient


@pytest.fixture(autouse=True)
def client(tmp_path, monkeypatch):
    db_file = tmp_path / "test_bank.db"
    monkeypatch.setenv("DB_PATH", str(db_file))
    # reload modules to pick up DB_PATH (reload repository then main)
    from importlib import import_module, reload
    repo = import_module("app.repository")
    # make sure repository reads the temp DB path
    reload(repo)
    # ensure the schema exists in the temp DB
    repo.init_db()
    mainmod = import_module("app.main")
    reload(mainmod)
    client = TestClient(mainmod.app)
    yield client


def test_create_and_deposit_and_balance(client):
    r = client.post("/accounts", json={"owner": "Alice"})
    assert r.status_code == 200
    acc = r.json()
    aid = acc["id"]

    r2 = client.post(f"/accounts/{aid}/deposit", json={"amount": 100.0})
    assert r2.status_code == 200
    assert r2.json()["balance"] == 100.0

    rb = client.get(f"/balances/{aid}")
    assert rb.status_code == 200
    assert rb.json()["balance"] == 100.0


def test_transfer(client):
    r1 = client.post("/accounts", json={"owner": "A"})
    r2 = client.post("/accounts", json={"owner": "B"})
    a1 = r1.json()["id"]
    a2 = r2.json()["id"]

    client.post(f"/accounts/{a1}/deposit", json={"amount": 50.0})
    t = client.post("/transfer", json={"from_id": a1, "to_id": a2, "amount": 20.0})
    assert t.status_code == 200

    b1 = client.get(f"/balances/{a1}").json()["balance"]
    b2 = client.get(f"/balances/{a2}").json()["balance"]
    assert b1 == 30.0
    assert b2 == 20.0
