"""Service layer implementing business rules for accounts.

Service methods are thin transaction scripts that orchestrate repository
calls and publish events for projections.
"""
from typing import Optional
from . import repository
from . import events


class InsufficientFunds(Exception):
    pass


class AccountService:
    def create_account(self, owner: str, initial_balance: float = 0.0) -> int:
        aid = repository.create_account(owner, initial_balance)
        # publish projection event
        events.publish({"type": "account_changed", "account_id": aid, "balance": float(initial_balance)})
        # synchronous projection for demo: also update read-model directly
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
