"""
Domain Model (Beginner-Friendly Explanation)
===========================================

This file defines the **domain layer** of the application.

In Domain-Driven Design and clean architecture, the *domain layer* is where the
core business rules and behaviors live. These classes represent the **real
world concepts** inside your system.

Here, our domain has two central concepts:

1. Message       → a single chat message
2. Conversation  → a collection of messages with rules/behavior

Why do we put behavior here instead of inside HTTP handlers?
------------------------------------------------------------
Because domain models:

- Are reusable in any environment (web, CLI, tests, AI pipelines)
- Keep business rules in one place
- Make the system easier to test
- Prevent duplication across routes or services

This is an evolution from Transaction Script → now logic lives inside objects,
NOT inside API handlers.
"""

from dataclasses import dataclass, field
from typing import List, Optional
import datetime


@dataclass
class Message:
    """
    DOMAIN ENTITY: A single message in a conversation.

    - sender: who sent the message
    - text: the content
    - created_at: timestamp (auto-set at creation)

    Note: This class has no database knowledge — that's intentional!
    The domain layer should NOT know about persistence.
    """
    sender: str
    text: str
    created_at: str = field(default_factory=lambda: datetime.datetime.utcnow().isoformat())


@dataclass
class Conversation:
    """
    DOMAIN ENTITY: A conversation holds multiple messages
    and has its own rules/behavior.

    Key points for beginners:
    -------------------------
    - This class defines what a conversation *is* (state)
    - It also defines what a conversation *can do* (behavior)
    - This separation of concerns is what makes this a Domain Model
    """
    id: Optional[int] = None
    title: str = ""
    messages: List[Message] = field(default_factory=list)
    closed: bool = False

    def add_message(self, sender: str, text: str) -> Message:
        """
        Domain Logic:
        -------------
        A conversation MUST NOT accept new messages if it is closed.

        This rule lives here because it belongs to the *business logic*,
        NOT the database or HTTP handler.
        """
        if self.closed:
            raise ValueError("Cannot add message to closed conversation")

        msg = Message(sender=sender, text=text)
        self.messages.append(msg)
        return msg

    def message_count(self) -> int:
        """Return how many messages are in this conversation."""
        return len(self.messages)

    def total_word_count(self) -> int:
        """Count the total number of words across all messages."""
        return sum(len(m.text.split()) for m in self.messages)

    def last_message(self) -> Optional[Message]:
        """Return the most recent message, or None if empty."""
        return self.messages[-1] if self.messages else None

    def close(self) -> None:
        """Mark conversation as closed (no new messages allowed)."""
        self.closed = True
