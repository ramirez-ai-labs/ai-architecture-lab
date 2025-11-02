from dataclasses import dataclass, field
from typing import List, Optional
import datetime


@dataclass
class Message:
    sender: str
    text: str
    created_at: str = field(default_factory=lambda: datetime.datetime.utcnow().isoformat())


@dataclass
class Conversation:
    id: Optional[int] = None
    title: str = ""
    messages: List[Message] = field(default_factory=list)
    closed: bool = False

    def add_message(self, sender: str, text: str) -> Message:
        """Add a message to the conversation. Raises ValueError if conversation is closed."""
        if self.closed:
            raise ValueError("Cannot add message to closed conversation")
        msg = Message(sender=sender, text=text)
        self.messages.append(msg)
        return msg

    def message_count(self) -> int:
        return len(self.messages)

    def total_word_count(self) -> int:
        return sum(len(m.text.split()) for m in self.messages)

    def last_message(self) -> Optional[Message]:
        return self.messages[-1] if self.messages else None

    def close(self) -> None:
        self.closed = True
