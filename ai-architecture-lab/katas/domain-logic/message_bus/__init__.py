"""
Message Bus Pattern Kata

A simple in-process event bus for coordinating domain events.
"""

from .message_bus import subscribe, publish, clear

__all__ = ['subscribe', 'publish', 'clear']
