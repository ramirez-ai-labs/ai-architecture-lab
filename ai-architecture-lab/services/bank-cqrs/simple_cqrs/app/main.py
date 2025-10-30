"""HTTP API wiring for the Bank CQRS minimal example.

This module maps HTTP requests to the Service Layer (AccountService).
It demonstrates the typical flow in a CQRS-style app:

- HTTP endpoint receives a command/query
- Endpoint calls Service methods to perform business logic (write side)
- Service updates the write-model via the repository and publishes events
- A projection (subscribed in startup) updates the read-model
- Query endpoints read from the read-model for fast responses

For learners: focus on the clear separation between command handling
 (endpoints that mutate state) and query endpoints that read the
 denormalized read-model.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

import os

from . import repository
from .service import AccountService, InsufficientFunds
from . import events

DB_PATH = os.getenv("DB_PATH", "./bank.db")

app = FastAPI(title="Bank CQRS - Minimal Example")

svc = AccountService()


class AccountIn(BaseModel):
    owner: str


class AccountOut(AccountIn):
    id: int
    balance: float


class TransferIn(BaseModel):
    from_id: int
    to_id: int
    amount: float


class AmountIn(BaseModel):
    amount: float


@app.on_event("startup")
def startup():
    # ensure DB and read-model exist
    repository.init_db()
    # register a simple, in-process projection: when an account changes,
    # update the denormalized read-model table. In production this would
    # usually be performed by asynchronous projection workers that
    # subscribe to events from a broker.
    def projection(event):
        if event.get("type") == "account_changed":
            repository.upsert_account_balance(event["account_id"], event["balance"])

    events.subscribe(projection)


@app.post("/accounts", response_model=AccountOut)
def create_account(payload: AccountIn):
    aid = svc.create_account(payload.owner)
    acc = repository.get_account(aid)
    return AccountOut(id=acc["id"], owner=acc["owner"], balance=acc["balance"])


@app.get("/accounts", response_model=List[AccountOut])
def list_accounts():
    rows = repository.list_accounts()
    return [AccountOut(id=r["id"], owner=r["owner"], balance=r["balance"]) for r in rows]


@app.get("/accounts/{account_id}", response_model=AccountOut)
def get_account(account_id: int):
    acc = repository.get_account(account_id)
    if not acc:
        raise HTTPException(status_code=404, detail="account not found")
    return AccountOut(id=acc["id"], owner=acc["owner"], balance=acc["balance"])


@app.post("/accounts/{account_id}/deposit")
def deposit(account_id: int, payload: AmountIn):
    try:
        new = svc.deposit(account_id, payload.amount)
    except KeyError:
        raise HTTPException(status_code=404, detail="account not found")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"id": account_id, "balance": new}


@app.post("/accounts/{account_id}/withdraw")
def withdraw(account_id: int, payload: AmountIn):
    try:
        new = svc.withdraw(account_id, payload.amount)
    except KeyError:
        raise HTTPException(status_code=404, detail="account not found")
    except InsufficientFunds:
        raise HTTPException(status_code=400, detail="insufficient funds")
    return {"id": account_id, "balance": new}


@app.post("/transfer")
def transfer(payload: TransferIn):
    try:
        svc.transfer(payload.from_id, payload.to_id, payload.amount)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except InsufficientFunds:
        raise HTTPException(status_code=400, detail="insufficient funds")
    return {"ok": True}


@app.get("/balances/{account_id}")
def get_balance(account_id: int):
    b = repository.get_account_balance(account_id)
    if b is None:
        raise HTTPException(status_code=404, detail="balance not found")
    return {"account_id": account_id, "balance": b}
