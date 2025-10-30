"""Simple in-process event bus for demo projections."""
from typing import Callable, Dict, List

_subscribers: List[Callable[[Dict], None]] = []


def subscribe(fn: Callable[[Dict], None]) -> None:
    _subscribers.append(fn)


def publish(event: Dict) -> None:
    # Synchronous publish to keep the example simple
    for s in list(_subscribers):
        try:
            s(event)
        except Exception:
            # projection errors shouldn't crash the writer in this demo
            pass
