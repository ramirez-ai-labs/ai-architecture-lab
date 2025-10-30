"""Repository (Table Data Gateway) for the Bank CQRS demo.

Encapsulates SQL and connection handling. The service layer uses this
module for persistence. The module also exposes a small read-model
projection function to keep the CQRS example simple and synchronous.
"""
import sqlite3
import os
from typing import Optional, Dict, List

DB_PATH = os.getenv("DB_PATH", "./bank.db")


def get_db_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_conn()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            owner TEXT NOT NULL,
            balance REAL NOT NULL
        )
        """
    )
    # read-model table (denormalized balances)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS account_balances (
            account_id INTEGER PRIMARY KEY,
            balance REAL NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


def create_account(owner: str, initial_balance: float = 0.0) -> int:
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO accounts (owner, balance) VALUES (?, ?)", (owner, float(initial_balance)))
    conn.commit()
    aid = cur.lastrowid
    conn.close()
    return aid


def get_account(account_id: int) -> Optional[Dict]:
    conn = get_db_conn()
    row = conn.execute("SELECT id, owner, balance FROM accounts WHERE id = ?", (account_id,)).fetchone()
    conn.close()
    if not row:
        return None
    return {"id": row["id"], "owner": row["owner"], "balance": row["balance"]}


def list_accounts() -> List[Dict]:
    conn = get_db_conn()
    rows = conn.execute("SELECT id, owner, balance FROM accounts ORDER BY id").fetchall()
    conn.close()
    return [{"id": r["id"], "owner": r["owner"], "balance": r["balance"]} for r in rows]


def upsert_account_balance(account_id: int, balance: float) -> None:
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO account_balances (account_id, balance) VALUES (?, ?) ON CONFLICT(account_id) DO UPDATE SET balance=excluded.balance", (account_id, float(balance)))
    conn.commit()
    conn.close()


def get_account_balance(account_id: int) -> Optional[float]:
    conn = get_db_conn()
    row = conn.execute("SELECT balance FROM account_balances WHERE account_id = ?", (account_id,)).fetchone()
    conn.close()
    if not row:
        return None
    return float(row["balance"])
