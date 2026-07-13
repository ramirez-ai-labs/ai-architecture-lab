"""
Examples demonstrating the Domain Model Kata

This module shows practical usage of the Message and Conversation classes.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from domain import Conversation


def example_basic_conversation():
    """Example 1: Create a conversation and add messages."""
    print("=== Example 1: Basic Conversation ===\n")
    
    conv = Conversation(title="Meeting Notes")
    print(f"Created conversation: {conv.title}")
    print(f"Is closed? {conv.closed}\n")
    
    # Add messages
    msg1 = conv.add_message("Alice", "Let's discuss the project")
    print(f"Alice added: {msg1.text}")
    
    msg2 = conv.add_message("Bob", "Good idea! What are priorities?")
    print(f"Bob added: {msg2.text}\n")
    
    print(f"Total messages: {conv.message_count()}")
    print(f"Total word count: {conv.total_word_count()}\n")


def example_closed_conversation():
    """Example 2: Try to add message to closed conversation."""
    print("=== Example 2: Closed Conversation ===\n")
    
    conv = Conversation(title="Archived Discussion")
    conv.add_message("Alice", "This is archived")
    print(f"Messages before closing: {conv.message_count()}")
    
    # Close the conversation
    conv.close()
    print(f"Conversation closed: {conv.closed}\n")
    
    # Try to add a message
    try:
        conv.add_message("Bob", "Can I still talk?")
    except ValueError as e:
        print(f"Error caught: {e}\n")


def example_last_message():
    """Example 3: Query the most recent message."""
    print("=== Example 3: Last Message Query ===\n")
    
    conv = Conversation(title="Support Chat")
    conv.add_message("User", "I need help")
    conv.add_message("Support", "How can we assist?")
    conv.add_message("User", "I have a bug report")
    
    last = conv.last_message()
    print(f"Last message sender: {last.sender}")
    print(f"Last message text: {last.text}")
    print(f"Timestamp: {last.created_at}\n")


if __name__ == "__main__":
    example_basic_conversation()
    example_closed_conversation()
    example_last_message()
    print("All examples completed!")
