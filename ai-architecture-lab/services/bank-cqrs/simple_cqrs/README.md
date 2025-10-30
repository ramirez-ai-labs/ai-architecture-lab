# Bank CQRS — Minimal example

This is a minimal, self-contained example demonstrating:

- Service Layer + Repository (Table Data Gateway)
- A tiny CQRS pattern: write model (accounts) and a denormalized read model (account_balances)
- A synchronous, in-process event projection that updates the read model after writes

Run locally (macOS / zsh):

```
cd ai-architecture-lab/services/bank-cqrs/simple_cqrs
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001
```

Endpoints (HTTP):
- POST /accounts {"owner": "Alice"} -> create account
- GET /accounts -> list accounts (write model)
- GET /accounts/{id} -> get account (write model)
- POST /accounts/{id}/deposit {"amount": 10.0}
- POST /transfer {"from_id":1, "to_id":2, "amount":5.0}
- GET /balances/{id} -> read-model balance (denormalized view)

This example keeps things intentionally small and synchronous so it is easy
to read and reason about. It is intended for learning the pattern, not for
production use.
