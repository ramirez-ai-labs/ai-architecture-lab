"""Simple in-process message bus for coordinating domain events.

A Message Bus (or Event Bus) is a core pattern for decoupled communication
between domain objects. When something important happens in your domain
(an order was placed, a payment succeeded, an account was created), you publish
an event to the bus rather than directly calling handlers. Subscribers listen
for events and react accordingly.

This kata demonstrates a synchronous, in-process message bus. It's ideal for:
- Learning the pattern with minimal complexity
- Single-process applications where all code runs in one interpreter
- Unit testing (no external broker to mock)

Production systems typically use a durable message broker (Kafka, RabbitMQ, AWS SNS/SQS)
for:
- Cross-service communication (events survive service restarts)
- Asynchronous, eventually-consistent workflows
- Event sourcing and audit trails

The contract is identical; only the transport changes. This kata gives you the concept.
"""
from typing import Any, Callable, Dict, List

# Subscribers are callables that accept an event dict
_subscribers: List[Callable[[Dict[str, Any]], None]] = []


def subscribe(handler: Callable[[Dict[str, Any]], None]) -> None:
    """Register a handler function to receive published events.

    Handlers are called synchronously in the order they were registered.

    Args:
        handler: A callable that accepts an event dict. The event dict should have
            at least a 'type' key identifying the event kind, plus domain-specific
            keys for payload (e.g., 'account_id', 'amount_cents').

    Example:
        >>> def on_account_created(event):
        ...     print(f"Account created: {event['account_id']}")
        >>> subscribe(on_account_created)
        >>> publish({'type': 'account_created', 'account_id': 123})
        Account created: 123
    """
    _subscribers.append(handler)


def publish(event: Dict[str, Any]) -> None:
    """Publish an event to all registered subscribers.

    Subscribers are called synchronously and in registration order. If a subscriber
    raises an exception, that exception propagates to the caller. This simplicity
    makes the pattern easy to understand and test.

    In production, you'd typically log failed subscriber invocations and continue
    (or use a dead-letter queue for retry). This demo prioritizes clarity over
    robustness.

    Args:
        event: An event dict. Should have a 'type' key and domain-specific
            keys for payload.

    Example:
        >>> def log_event(event):
        ...     print(f"Event: {event['type']}")
        >>> subscribe(log_event)
        >>> publish({'type': 'payment_succeeded', 'amount_cents': 5000})
        Event: payment_succeeded
    """
    for handler in list(_subscribers):
        handler(event)


def clear() -> None:
    """Clear all subscribers. Useful for test cleanup.

    Example:
        >>> subscribe(lambda e: None)
        >>> clear()
        >>> # Now no subscribers are registered
    """
    global _subscribers
    _subscribers = []
