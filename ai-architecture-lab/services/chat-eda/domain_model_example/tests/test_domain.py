import pytest
from app.domain import Conversation


def test_add_message_and_counts():
    c = Conversation(title="Test")
    c.add_message("alice", "hello world")
    c.add_message("bob", "hi")
    assert c.message_count() == 2
    assert c.total_word_count() == 3


def test_close_prevents_add():
    c = Conversation()
    c.close()
    with pytest.raises(ValueError):
        c.add_message("a", "b")
