import sqlite3
from typing import Optional, List
from .domain import Conversation, Message


class ConversationRepository:
    """Simple Data Mapper / Repository using sqlite3.

    This mapper stores conversations and messages in two tables. It's intentionally
    straightforward for instructional purposes.
    """

    def __init__(self, db_path: str = "./conversations.db"):
        self.db_path = db_path
        self._ensure_tables()

    def _conn(self):
        return sqlite3.connect(self.db_path)

    def _ensure_tables(self):
        with self._conn() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT,
                    closed INTEGER
                )
                """
            )
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    conversation_id INTEGER,
                    sender TEXT,
                    text TEXT,
                    created_at TEXT,
                    FOREIGN KEY(conversation_id) REFERENCES conversations(id)
                )
                """
            )

    def save(self, conv: Conversation) -> Conversation:
        with self._conn() as conn:
            cur = conn.cursor()
            if conv.id is None:
                cur.execute(
                    "INSERT INTO conversations (title, closed) VALUES (?,?)",
                    (conv.title, int(conv.closed)),
                )
                conv.id = cur.lastrowid
            else:
                cur.execute(
                    "UPDATE conversations SET title=?, closed=? WHERE id=?",
                    (conv.title, int(conv.closed), conv.id),
                )
                # remove existing messages and re-insert (simple approach)
                cur.execute("DELETE FROM messages WHERE conversation_id=?", (conv.id,))

            for m in conv.messages:
                cur.execute(
                    "INSERT INTO messages (conversation_id, sender, text, created_at) VALUES (?,?,?,?)",
                    (conv.id, m.sender, m.text, m.created_at),
                )

        return conv

    def get(self, conv_id: int) -> Optional[Conversation]:
        conn = self._conn()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM conversations WHERE id=?", (conv_id,))
        row = cur.fetchone()
        if not row:
            return None
        conv = Conversation(id=row["id"], title=row["title"], closed=bool(row["closed"]))
        cur.execute(
            "SELECT sender, text, created_at FROM messages WHERE conversation_id=? ORDER BY id",
            (conv.id,),
        )
        for r in cur.fetchall():
            conv.messages.append(Message(sender=r["sender"], text=r["text"], created_at=r["created_at"]))
        conn.close()
        return conv

    def list_all(self) -> List[Conversation]:
        conn = self._conn()
        cur = conn.cursor()
        cur.execute("SELECT id FROM conversations ORDER BY id")
        ids = [r[0] for r in cur.fetchall()]
        conn.close()
        return [self.get(i) for i in ids]
