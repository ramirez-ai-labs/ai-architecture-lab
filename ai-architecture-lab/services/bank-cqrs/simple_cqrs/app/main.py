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

    # register a simple projection: when an account changes, update read model
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
