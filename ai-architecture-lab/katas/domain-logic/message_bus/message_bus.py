"""Simple in-process message bus for coordinating domain events.

WHAT IS A MESSAGE BUS?
A Message Bus (or Event Bus) is a core pattern for decoupled communication
between domain objects. When something important happens in your domain
(an order was placed, a payment succeeded, an account was created), you publish
an event to the bus rather than directly calling handlers. Subscribers listen
for events and react accordingly.

THE DECOUPLING BENEFIT:
Without Message Bus, domain logic calls handlers directly (tightly coupled):
    account.create()
    send_confirmation_email()      # Direct call to infrastructure
    update_inventory()             # Direct call
    log_analytics()                # Direct call

With Message Bus (decoupled):
    account.create()
    publish({'type': 'account_created', 'account_id': 123})
    # Email, inventory, analytics handlers listen and react independently

This kata demonstrates a synchronous, in-process message bus. It's ideal for:
- Learning the pattern with minimal complexity
- Single-process applications where all code runs in one interpreter
- Unit testing (no external broker to mock)

PRODUCTION SYSTEMS:
Use a durable message broker (Kafka, RabbitMQ, AWS SNS/SQS) when you need:
- Cross-service communication (events survive service restarts)
- Asynchronous, eventually-consistent workflows
- Event sourcing (store and replay all events)
- Audit trails and compliance logging

The contract is identical; only the transport changes. This kata gives you the concept.
"""
from typing import Any, Callable, Dict, List

# Subscribers are callables that accept an event dict
_subscribers: List[Callable[[Dict[str, Any]], None]] = []


def subscribe(handler: Callable[[Dict[str, Any]], None]) -> None:
    """Register a handler function to receive published events.

    WHAT DOES SUBSCRIBE DO?
    subscribe() registers a handler function with the message bus.
    Whenever an event is published, this handler will be called with that event.

    EXECUTION ORDER:
    Handlers are called synchronously in the order they were registered.
    If you subscribe(handler_A) then subscribe(handler_B), then:
    - When an event is published, handler_A is called first
    - Then handler_B is called
    - Then control returns to the publisher

    HANDLER FUNCTION SIGNATURE:
    A handler is a callable that takes an event dict and returns None.
    Handler should check the event type and react accordingly.
    Example handler:
        def on_account_created(event):
            if event['type'] == 'account_created':
                send_welcome_email(event['account_id'])

    EVENT DICT STRUCTURE:
    By convention, events should have a 'type' key identifying the event kind.
    Additional keys contain the payload:
        {
            'type': 'account_created',           # Convention: event type
            'account_id': 123,                   # Payload: domain data
            'email': 'alice@example.com',        # Payload: additional data
            'timestamp': '2026-07-07T10:00:00Z', # Payload: metadata
        }

    EXAMPLE:
        >>> # Define a handler that reacts to account creation events
        >>> def on_account_created(event):
        ...     if event['type'] == 'account_created':
        ...         print(f"Account created: {event['account_id']}")
        ...
        >>> # Register the handler with the bus
        >>> subscribe(on_account_created)
        ...
        >>> # Publish an event (handler will be called)
        >>> publish({'type': 'account_created', 'account_id': 123})
        Account created: 123

    Args:
        handler: A callable that accepts an event dict. The handler should:
            - Accept one parameter: the event dict
            - Return None (not expected to return a value)
            - Check event['type'] if it only handles certain event types
            - Raise an exception if something goes wrong (no error recovery in this bus)

    Returns:
        None. The handler is registered globally and called on future publishes.
    """
    # Add the handler to the global list of subscribers
    # When publish() is called, each handler in this list will be invoked
    _subscribers.append(handler)


def publish(event: Dict[str, Any]) -> None:
    """Publish an event to all registered subscribers.

    WHAT DOES PUBLISH DO?
    publish() announces that something happened. All handlers registered with
    subscribe() will be notified (called) with the event details.

    EXECUTION FLOW:
    1. Publisher calls publish({'type': 'account_created', 'account_id': 123})
    2. Message bus calls each handler in registration order
    3. Each handler receives the event dict and can react
    4. After all handlers are called, control returns to the publisher

    SYNCHRONOUS EXECUTION:
    This is a synchronous bus (handlers run immediately, blocking the publisher).
    The publisher waits for all handlers to finish before continuing.
    This is simple but means slow handlers slow down everything.
    Production systems use asynchronous brokers (Kafka, RabbitMQ) where
    the publisher doesn't wait for handlers to finish.

    ERROR HANDLING IN THIS SIMPLE BUS:
    If a handler raises an exception, it propagates to the caller.
    Subsequent handlers are NOT called (execution stops).
    This simplicity makes the bus easy to understand and test.

    In production, you'd want to:
    - Log failed handler invocations
    - Continue calling other handlers even if one fails
    - Use a dead-letter queue to retry failed handlers
    - Implement backoff and retry logic

    But this simple bus prioritizes clarity over robustness.

    DEFENSIVE COPY OF SUBSCRIBERS:
    We call list(_subscribers) to make a copy of the subscriber list.
    This allows handlers to subscribe/unsubscribe without breaking the iteration.
    (Though in this simple bus, we don't support unsubscribe.)

    EXAMPLE:
        >>> # Set up handlers
        >>> def update_read_model(event):
        ...     print(f"Updating read model for {event['type']}")
        >>> def send_notification(event):
        ...     print(f"Sending notification for {event['type']}")
        >>> subscribe(update_read_model)
        >>> subscribe(send_notification)
        ...
        >>> # Publish an event (both handlers are called)
        >>> publish({'type': 'order_created', 'order_id': 456})
        Updating read model for order_created
        Sending notification for order_created

    Args:
        event: An event dict representing something that happened.
            Should follow the convention of having a 'type' key and
            domain-specific keys for the payload.
            Example: {
                'type': 'payment_processed',
                'payment_id': 'PAY123',
                'amount_cents': 10000,
                'account_id': 'ACC456',
            }

    Returns:
        None. Does not return a value; handlers' return values are ignored.

    Raises:
        Any exception raised by a handler (no error recovery in this simple bus).
    """
    # Make a copy of _subscribers list in case handlers modify it
    # Iterate through each registered handler
    for handler in list(_subscribers):
        # Call the handler with the event
        # Handler is responsible for checking event['type'] if needed
        handler(event)


def clear() -> None:
    """Clear all subscribers. Useful for test cleanup between test cases.

    WHY IS THIS NEEDED?
    The message bus stores subscribers in a global variable (_subscribers).
    This means subscribers persist across multiple function calls.
    In unit tests, if one test subscribes a handler, the next test will
    still have that handler registered, causing unexpected behavior.

    SOLUTION: clear() removes all handlers.
    Call this at the beginning or end of each test to ensure a clean slate.

    EXAMPLE (test setup):
        >>> def test_account_creation():
        ...     # Start with no subscribers
        ...     clear()
        ...
        ...     events_captured = []
        ...     def capture_event(event):
        ...         events_captured.append(event)
        ...
        ...     subscribe(capture_event)
        ...     publish({'type': 'account_created'})
        ...
        ...     # Verify the event was captured
        ...     assert len(events_captured) == 1
        ...
        ...     # Clean up for the next test
        ...     clear()

    Returns:
        None. Removes all handlers from the global subscriber list.
    """
    global _subscribers
    # Empty the global list of subscribers
    # All handlers are discarded
    _subscribers = []
