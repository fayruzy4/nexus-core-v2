from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import TypeAlias, TypeVar

from app.core.events.event import BaseEvent

EventT = TypeVar("EventT", bound=BaseEvent)

EventListener: TypeAlias = Callable[[EventT], Awaitable[None]]

__all__ = [
    "EventT",
    "EventListener",
]
