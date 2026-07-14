from __future__ import annotations

from app.core.events.bus import event_bus
from app.core.events.event import BaseEvent


async def publish(event: BaseEvent) -> None:
    """
    Publish an event to the internal Event Bus.
    """
    await event_bus.publish(event)


__all__ = [
    "publish",
]
