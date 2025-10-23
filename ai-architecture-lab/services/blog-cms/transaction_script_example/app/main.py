"""Transaction Script demo (Blog CMS).

Key idea: Domain logic is implemented as Transaction Scripts.
Each HTTP handler is a small, explicit procedure that:
    1) opens a DB connection, 2) runs SQL, 3) commits/closes, 4) returns a
         simple DTO. That mapping makes it obvious what each request does.

Where this pattern is a good fit:
- Small apps or admin/UIs with simple CRUD flows.
- When you want the request flow to be easy to read and debug.

When to refactor away from Transaction Script:
- As logic grows, move shared rules into service functions or a domain
    layer to avoid duplication and to improve testability.

Notes:
- `DB_PATH` (env) controls the SQLite file (default: ./posts.db).
- Tests set `DB_PATH` to a temp file and reload this module to create
    an isolated DB for each test run.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
from typing import List, Optional
import os

# DB path can be overridden by environment (useful for tests)
DB_PATH = os.getenv("DB_PATH", "./posts.db")

app = FastAPI(title="Blog CMS - Transaction Script Example")


class PostIn(BaseModel):
    title: str
    content: str


class PostOut(PostIn):
    id: int


def get_db_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_conn()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


# Ensure DB is initialized when module is imported (tests set DB_PATH before reload)
try:
    init_db()
except Exception:
    # ignore errors during import-time init (e.g., invalid path during import)
    pass


@app.on_event("startup")
def startup():
    init_db()


@app.post("/posts", response_model=PostOut)
def create_post(post: PostIn):
    # Transaction Script: the handler itself is the transaction script.
    # Steps: open connection, execute SQL, commit, return DTO.
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)", (post.title, post.content))
    conn.commit()
    post_id = cur.lastrowid
    conn.close()
    return {"id": post_id, "title": post.title, "content": post.content}


@app.get("/posts", response_model=List[PostOut])
def list_posts():
    # Transaction Script for listing: read-only script that returns DTOs.
    conn = get_db_conn()
    rows = conn.execute("SELECT id, title, content FROM posts ORDER BY id DESC").fetchall()
    conn.close()
    return [PostOut(id=r["id"], title=r["title"], content=r["content"]) for r in rows]


@app.get("/posts/{post_id}", response_model=PostOut)
def get_post(post_id: int):
    # Transaction Script: single-row read and DTO mapping.
    conn = get_db_conn()
    row = conn.execute("SELECT id, title, content FROM posts WHERE id = ?", (post_id,)).fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Post not found")
    return PostOut(id=row["id"], title=row["title"], content=row["content"])


@app.put("/posts/{post_id}", response_model=PostOut)
def update_post(post_id: int, post: PostIn):
    # Transaction Script: update within one procedural handler.
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute("UPDATE posts SET title = ?, content = ? WHERE id = ?", (post.title, post.content, post_id))
    if cur.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Post not found")
    conn.commit()
    conn.close()
    return {"id": post_id, "title": post.title, "content": post.content}


@app.delete("/posts/{post_id}")
def delete_post(post_id: int):
    # Transaction Script: delete operation handled entirely in the handler.
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM posts WHERE id = ?", (post_id,))
    if cur.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Post not found")
    conn.commit()
    conn.close()
    return {"deleted": True}
