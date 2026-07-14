from __future__ import annotations

from typing import Protocol

from app.core.events.event import BaseEvent


class EventListener(Protocol):
    """
    Protocol for event listeners.

    A listener is any async callable that accepts a BaseEvent.
    """

    async def __call__(self, event: BaseEvent) -> None:
        ...
