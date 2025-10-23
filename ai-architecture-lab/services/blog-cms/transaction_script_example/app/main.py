from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
from typing import List, Optional
import os

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
    # Transaction Script: procedural logic per request
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)", (post.title, post.content))
    conn.commit()
    post_id = cur.lastrowid
    conn.close()
    return {"id": post_id, "title": post.title, "content": post.content}


@app.get("/posts", response_model=List[PostOut])
def list_posts():
    conn = get_db_conn()
    rows = conn.execute("SELECT id, title, content FROM posts ORDER BY id DESC").fetchall()
    conn.close()
    return [PostOut(id=r["id"], title=r["title"], content=r["content"]) for r in rows]


@app.get("/posts/{post_id}", response_model=PostOut)
def get_post(post_id: int):
    conn = get_db_conn()
    row = conn.execute("SELECT id, title, content FROM posts WHERE id = ?", (post_id,)).fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Post not found")
    return PostOut(id=row["id"], title=row["title"], content=row["content"])


@app.put("/posts/{post_id}", response_model=PostOut)
def update_post(post_id: int, post: PostIn):
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
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM posts WHERE id = ?", (post_id,))
    if cur.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Post not found")
    conn.commit()
    conn.close()
    return {"deleted": True}
