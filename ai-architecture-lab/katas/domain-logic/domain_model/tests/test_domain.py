"""
Unit tests for Domain Model Kata

These tests verify the core business logic of the domain model without
any dependencies on databases, HTTP frameworks, or external services.
"""

import pytest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from domain import Message, Conversation


class TestMessage:
    """Test cases for the Message domain entity."""
    
    def test_message_creation(self):
        """Test creating a message with basic fields."""
        msg = Message(sender="Alice", text="Hello world")
        
        assert msg.sender == "Alice"
        assert msg.text == "Hello world"
        assert msg.created_at is not None
    
    def test_message_timestamp_format(self):
        """Test that created_at is in ISO format."""
        msg = Message(sender="Bob", text="Test message")
        
        # ISO format should have 'T' separator
        assert "T" in msg.created_at or "-" in msg.created_at


class TestConversation:
    """Test cases for the Conversation domain entity."""
    
    def test_conversation_creation(self):
        """Test creating an empty conversation."""
        conv = Conversation(title="Test Chat")
        
        assert conv.title == "Test Chat"
        assert conv.messages == []
        assert conv.closed is False
        assert conv.message_count() == 0
    
    def test_add_message(self):
        """Test adding a message to a conversation."""
        conv = Conversation(title="Chat")
        msg = conv.add_message("Alice", "Hi there")
        
        assert isinstance(msg, Message)
        assert msg.sender == "Alice"
        assert msg.text == "Hi there"
        assert conv.message_count() == 1
    
    def test_add_multiple_messages(self):
        """Test adding multiple messages."""
        conv = Conversation(title="Chat")
        
        conv.add_message("Alice", "Hello")
        conv.add_message("Bob", "Hi Alice")
        conv.add_message("Alice", "How are you?")
        
        assert conv.message_count() == 3
    
    def test_last_message_returns_most_recent(self):
        """Test that last_message() returns the newest message."""
        conv = Conversation(title="Chat")
        
        msg1 = conv.add_message("Alice", "First")
        msg2 = conv.add_message("Bob", "Second")
        msg3 = conv.add_message("Charlie", "Third")
        
        last = conv.last_message()
        assert last == msg3
        assert last.sender == "Charlie"
    
    def test_last_message_empty_conversation(self):
        """Test that last_message() returns None for empty conversation."""
        conv = Conversation(title="Empty Chat")
        
        assert conv.last_message() is None
    
    def test_close_conversation(self):
        """Test closing a conversation."""
        conv = Conversation(title="Chat")
        
        assert conv.closed is False
        conv.close()
        assert conv.closed is True
    
    def test_cannot_add_message_to_closed_conversation(self):
        """Test that adding message to closed conversation raises error."""
        conv = Conversation(title="Chat")
        conv.add_message("Alice", "First message")
        conv.close()
        
        with pytest.raises(ValueError, match="Cannot add message to closed conversation"):
            conv.add_message("Bob", "Should fail")
    
    def test_total_word_count(self):
        """Test calculating total word count across all messages."""
        conv = Conversation(title="Chat")
        
        conv.add_message("Alice", "One two three")  # 3 words
        conv.add_message("Bob", "Four five")         # 2 words
        
        assert conv.total_word_count() == 5
    
    def test_total_word_count_empty_conversation(self):
        """Test word count for empty conversation."""
        conv = Conversation(title="Chat")
        
        assert conv.total_word_count() == 0
    
    def test_conversation_state_isolation(self):
        """Test that multiple conversations don't share state."""
        conv1 = Conversation(title="Chat 1")
        conv2 = Conversation(title="Chat 2")
        
        conv1.add_message("Alice", "In chat 1")
        conv2.add_message("Bob", "In chat 2")
        
        assert conv1.message_count() == 1
        assert conv2.message_count() == 1
        assert conv1.messages[0].sender == "Alice"
        assert conv2.messages[0].sender == "Bob"
    
    def test_conversation_with_optional_id(self):
        """Test creating conversation with optional ID."""
        conv1 = Conversation(id=None, title="No ID")
        conv2 = Conversation(id=42, title="With ID")
        
        assert conv1.id is None
        assert conv2.id == 42
    
    def test_add_message_returns_message_object(self):
        """Test that add_message returns the Message object."""
        conv = Conversation(title="Chat")
        result = conv.add_message("Alice", "Test")
        
        assert isinstance(result, Message)
        assert result in conv.messages
    
    def test_message_order_preserved(self):
        """Test that messages are stored in order."""
        conv = Conversation(title="Chat")
        
        msg1 = conv.add_message("Alice", "First")
        msg2 = conv.add_message("Bob", "Second")
        msg3 = conv.add_message("Charlie", "Third")
        
        assert conv.messages[0] == msg1
        assert conv.messages[1] == msg2
        assert conv.messages[2] == msg3


class TestIntegration:
    """Integration tests combining multiple features."""
    
    def test_full_conversation_lifecycle(self):
        """Test a complete conversation workflow."""
        # Create conversation
        conv = Conversation(id=1, title="Support Chat")
        assert not conv.closed
        
        # Add messages
        conv.add_message("Customer", "I have an issue")
        conv.add_message("Support", "What is the problem?")
        conv.add_message("Customer", "My app crashed")
        
        # Check state
        assert conv.message_count() == 3
        assert conv.total_word_count() > 0
        assert conv.last_message().sender == "Customer"
        
        # Close conversation
        conv.close()
        assert conv.closed
        
        # Verify no more messages can be added
        with pytest.raises(ValueError):
            conv.add_message("Customer", "One more thing")
    
    def test_multiple_senders_conversation(self):
        """Test conversation with multiple participants."""
        conv = Conversation(title="Team Discussion")
        
        participants = ["Alice", "Bob", "Charlie", "Diana"]
        messages = [
            "What's the plan?",
            "Let's start with analysis",
            "I suggest we use Design Pattern X",
            "Good idea! I'll research it"
        ]
        
        for sender, text in zip(participants, messages):
            conv.add_message(sender, text)
        
        assert conv.message_count() == 4
        
        # Verify all senders are present
        senders = [msg.sender for msg in conv.messages]
        assert senders == participants
