from __future__ import annotations

from app.core.events.bus import event_bus
from app.core.events.event import BaseEvent
from app.core.events.types import EventListener


def subscribe(
    event_type: type[BaseEvent],
    listener: EventListener,
) -> None:
    """
    Register an event listener.
    """
    event_bus.subscribe(
        event_type=event_type,
        listener=listener,
    )


def unsubscribe(
    event_type: type[BaseEvent],
    listener: EventListener,
) -> None:
    """
    Unregister an event listener.
    """
    event_bus.unsubscribe(
        event_type=event_type,
        listener=listener,
    )


__all__ = [
    "subscribe",
    "unsubscribe",
]
