import os
from pathlib import Path

import pytest

from app.domain import Conversation
from app.repository import ConversationRepository


def test_save_and_get(tmp_path):
    db = tmp_path / "test.db"
    repo = ConversationRepository(str(db))

    conv = Conversation(title="Demo")
    conv.add_message("alice", "hello")
    conv.add_message("bot", "response here")

    saved = repo.save(conv)
    assert saved.id is not None

    loaded = repo.get(saved.id)
    assert loaded is not None
    assert loaded.title == "Demo"
    assert loaded.message_count() == 2
    assert loaded.total_word_count() == 3


def test_list_all(tmp_path):
    db = tmp_path / "test2.db"
    repo = ConversationRepository(str(db))
    c1 = Conversation(title="A")
    c1.add_message("x", "one")
    repo.save(c1)
    c2 = Conversation(title="B")
    c2.add_message("y", "two words")
    repo.save(c2)

    all_conv = repo.list_all()
    assert len(all_conv) == 2
