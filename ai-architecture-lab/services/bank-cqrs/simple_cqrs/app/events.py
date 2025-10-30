"""Simple in-process event bus for demo projections.

This is a tiny synchronous event bus used only for the demo so we can
illustrate the flow: write-model mutation -> event publish -> projection
update of a read-model. In production you'd normally publish events to
a durable broker (Kafka, RabbitMQ, etc.) and run projection workers
that handle events asynchronously (eventual consistency).

Keep the bus intentionally tiny so learners can follow the entire
path without external infra.
"""
from typing import Callable, Dict, List

# Subscribers are simple callables that accept an event dict.
_subscribers: List[Callable[[Dict], None]] = []


def subscribe(fn: Callable[[Dict], None]) -> None:
    """Register a projection or handler function to receive published events.

    Note: subscribers are called synchronously in this demo.
    """
    _subscribers.append(fn)


def publish(event: Dict) -> None:
    """Publish an event to all subscribers synchronously.

    We swallow exceptions here so a failing projection does not crash the
    writer in this toy example. In a real system you'd want visibility
    into projection failures and a retry strategy.
    """
    # Synchronous publish to keep the example simple
    for s in list(_subscribers):
        try:
            s(event)
        except Exception:
            # projection errors shouldn't crash the writer in this demo
            pass
