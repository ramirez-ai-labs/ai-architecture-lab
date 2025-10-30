"""Service layer implementing business rules for accounts.

This module shows a simple Service Layer: each method implements a unit
of business logic (create, deposit, withdraw, transfer). The Service
Layer coordinates repository calls (persistence) and publishes events
for projections (read-model updates).

Notes for learners:
- Inputs/outputs: methods accept primitive types and return simple
    values (ids or balances). Errors are raised for invalid inputs or
    business rule violations (eg. insufficient funds).
- Transaction handling: for simplicity we open and commit sqlite
    transactions directly here via the repository. In a larger app you'd
    move transactional boundaries to a dedicated unit-of-work.
- Events: we publish events after write-model changes. The demo uses a
    synchronous in-process projection so the read-model is updated
    immediately; in real-world CQRS you may have async/eventual
    consistency via a message broker.
"""
from typing import Optional
from . import repository
from . import events


class InsufficientFunds(Exception):
    pass


class AccountService:
    def create_account(self, owner: str, initial_balance: float = 0.0) -> int:
        # write-model: insert the account row and return its id
        aid = repository.create_account(owner, initial_balance)

        # publish an event describing what changed. In a real system this
        # would be emitted to a broker so other services/workers could
        # react asynchronously.
        events.publish({"type": "account_changed", "account_id": aid, "balance": float(initial_balance)})

        # For this small demo we also update the read-model synchronously
        # so queries immediately reflect the change. This keeps the
        # example deterministic and easy to follow for learners.
        repository.upsert_account_balance(aid, float(initial_balance))
        return aid

    def deposit(self, account_id: int, amount: float) -> float:
        if amount <= 0:
            raise ValueError("deposit amount must be positive")
        conn = repository.get_db_conn()
        try:
            cur = conn.cursor()
            cur.execute("SELECT balance FROM accounts WHERE id = ?", (account_id,))
            row = cur.fetchone()
            if not row:
                raise KeyError("account not found")
            new_balance = float(row[0]) + float(amount)
            cur.execute("UPDATE accounts SET balance = ? WHERE id = ?", (new_balance, account_id))
            conn.commit()
        finally:
            conn.close()

        # After mutating the write-model, publish an event and update the
        # read-model so queries can read the new balance. The event allows
        # decoupled projections in a real system; here it co-exists with a
        # direct upsert for simplicity.
        events.publish({"type": "account_changed", "account_id": account_id, "balance": new_balance})
        repository.upsert_account_balance(account_id, new_balance)
        return new_balance

    def withdraw(self, account_id: int, amount: float) -> float:
        if amount <= 0:
            raise ValueError("withdraw amount must be positive")
        conn = repository.get_db_conn()
        try:
            cur = conn.cursor()
            cur.execute("SELECT balance FROM accounts WHERE id = ?", (account_id,))
            row = cur.fetchone()
            if not row:
                raise KeyError("account not found")
            current = float(row[0])
            if current < amount:
                raise InsufficientFunds("insufficient funds")
            new_balance = current - float(amount)
            cur.execute("UPDATE accounts SET balance = ? WHERE id = ?", (new_balance, account_id))
            conn.commit()
        finally:
            conn.close()

        events.publish({"type": "account_changed", "account_id": account_id, "balance": new_balance})
        repository.upsert_account_balance(account_id, new_balance)
        return new_balance

    def transfer(self, from_id: int, to_id: int, amount: float) -> None:
        if amount <= 0:
            raise ValueError("transfer amount must be positive")
        conn = repository.get_db_conn()
        try:
            cur = conn.cursor()
            # check from
            cur.execute("SELECT balance FROM accounts WHERE id = ?", (from_id,))
            r1 = cur.fetchone()
            if not r1:
                raise KeyError("from account not found")
            cur.execute("SELECT balance FROM accounts WHERE id = ?", (to_id,))
            r2 = cur.fetchone()
            if not r2:
                raise KeyError("to account not found")
            if float(r1[0]) < amount:
                raise InsufficientFunds("insufficient funds")
            new_from = float(r1[0]) - float(amount)
            new_to = float(r2[0]) + float(amount)
            cur.execute("UPDATE accounts SET balance = ? WHERE id = ?", (new_from, from_id))
            cur.execute("UPDATE accounts SET balance = ? WHERE id = ?", (new_to, to_id))
            conn.commit()
        finally:
            conn.close()

        # publish events for both accounts and update read-model synchronously
        events.publish({"type": "account_changed", "account_id": from_id, "balance": new_from})
        events.publish({"type": "account_changed", "account_id": to_id, "balance": new_to})
        repository.upsert_account_balance(from_id, new_from)
        repository.upsert_account_balance(to_id, new_to)
