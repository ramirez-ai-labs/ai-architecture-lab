"""
Repository Pattern (Beginner Explanation)
=========================================

This file shows the **Repository pattern**, which is the next step
beyond Transaction Script.

Why a Repository?
-----------------
A Repository is like a "storage service" that:

- Loads domain objects from the database
- Saves domain objects back to the database
- Hides SQL details from the rest of the application

This is why:
- The domain model does NOT contain SQL
- The API layer does NOT contain SQL
- Only the Repository knows how to talk to SQLite

Think of it as a translator:
    Domain Model <--> Repository <--> Database

This is the pattern used in MOST modern backend systems.
"""

import sqlite3
from typing import Optional, List
from .domain import Conversation, Message


class ConversationRepository:
    """
    Simple Repository for storing and retrieving Conversation objects.

    Key beginner concepts:
    ----------------------
    - This class isolates *all* database operations
    - The rest of the app uses ONLY domain objects, never SQL
    - Domain models stay clean and reusable
    """

    def __init__(self, db_path: str = "./conversations.db"):
        self.db_path = db_path
        self._ensure_tables()

    def _conn(self):
        """Create a new SQLite connection. SQLite stores everything in one file."""
        return sqlite3.connect(self.db_path)

    def _ensure_tables(self):
        """
        Create tables if they don't exist yet.

        This is intentionally simple — real systems might use migrations.
        """
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

    # ======================================================================
    # SAVE OPERATION (Insert or Update a Conversation)
    # ======================================================================
    def save(self, conv: Conversation) -> Conversation:
        """
        Save a Conversation + its messages to the database.

        Beginner notes:
        ---------------
        - If conv.id is None → it's new, so INSERT it.
        - Otherwise UPDATE existing row.
        - Messages are deleted & re-inserted (simple but not optimal)
        """
        with self._conn() as conn:
            cur = conn.cursor()

            if conv.id is None:
                # Insert new conversation
                cur.execute(
                    "INSERT INTO conversations (title, closed) VALUES (?, ?)",
                    (conv.title, int(conv.closed)),
                )
                conv.id = cur.lastrowid

            else:
                # Update existing conversation
                cur.execute(
                    "UPDATE conversations SET title=?, closed=? WHERE id=?",
                    (conv.title, int(conv.closed), conv.id),
                )
                # Simplest approach: wipe messages & re-add
                cur.execute("DELETE FROM messages WHERE conversation_id=?", (conv.id,))

            # Insert messages
            for m in conv.messages:
                cur.execute(
                    """
                    INSERT INTO messages (conversation_id, sender, text, created_at)
                    VALUES (?, ?, ?, ?)
                    """,
                    (conv.id, m.sender, m.text, m.created_at),
                )

        return conv

    # ======================================================================
    # LOAD ONE CONVERSATION
    # ======================================================================
    def get(self, conv_id: int) -> Optional[Conversation]:
        """
        Load a Conversation and all its messages.

        Beginner notes:
        ---------------
        - Repo loads raw SQL rows
        - Converts them into domain objects
        - Returns a fully-populated Conversation
        """
        conn = self._conn()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        # First load the conversation row
        cur.execute("SELECT * FROM conversations WHERE id=?", (conv_id,))
        row = cur.fetchone()

        if not row:
            conn.close()
            return None

        conv = Conversation(
            id=row["id"],
            title=row["title"],
            closed=bool(row["closed"]),
        )

        # Now load all associated messages
        cur.execute(
            """
            SELECT sender, text, created_at
            FROM messages
            WHERE conversation_id=?
            ORDER BY id
            """,
            (conv.id,),
        )

        for r in cur.fetchall():
            conv.messages.append(
                Message(sender=r["sender"], text=r["text"], created_at=r["created_at"])
            )

        conn.close()
        return conv

    # ======================================================================
    # LIST ALL CONVERSATIONS
    # ======================================================================
    def list_all(self) -> List[Conversation]:
        """
        Return a list of ALL conversations by ID.

        We then hydrate each Conversation using get().
        """
        conn = self._conn()
        cur = conn.cursor()

        cur.execute("SELECT id FROM conversations ORDER BY id")
        ids = [r[0] for r in cur.fetchall()]
        conn.close()

        return [self.get(i) for i in ids]
