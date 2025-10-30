# Bank CQRS — Minimal example

Summary
-------
Minimal, self-contained demo illustrating Service Layer + Repository and a tiny CQRS pattern: a normalized write-model (`accounts`) and a denormalized read-model (`account_balances`) maintained by a simple in-process projection.

What this demonstrates
-----------------------
- Service Layer (business logic) separated from persistence (Table Data Gateway)
- Denormalized read-model for fast queries (CQRS-style)
- Event publication and a synchronous projection for easy-to-follow flow

Tech
----
- Python 3.11+, FastAPI, Uvicorn, SQLite (builtin)

Quick start (macOS / zsh)
------------------------
Run the example locally from the repo root:

```bash
cd ai-architecture-lab/services/bank-cqrs/simple_cqrs
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001
```

HTTP endpoints
--------------
- POST /accounts                — create account (body: {"owner": "Alice"})
- GET  /accounts                — list accounts (from write-model)
- GET  /accounts/{id}           — get account (from write-model)
- POST /accounts/{id}/deposit   — deposit to account (body: {"amount": 10.0})
- POST /transfer                — transfer between accounts (body: {"from_id":1, "to_id":2, "amount":5.0})
- GET  /balances/{id}           — read-model balance (denormalized view)

Notes for learners
------------------
- The example intentionally updates the read-model synchronously so the projection is easy to follow and tests are deterministic. In production you would typically publish events to a broker and project asynchronously (eventual consistency).
- The `DB_PATH` environment variable controls where the SQLite file is written (default: `./bank.db`). Tests override this to use temporary DB files.

Tests
-----
Install dev deps and run pytest from the example folder (or use the repo top-level `PYTHONPATH=.` pattern used by the other examples):

```bash
source .venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=. pytest -q
```

This repository contains both integration and unit tests; unit tests mock the repository and event bus to exercise the Service Layer in isolation.
