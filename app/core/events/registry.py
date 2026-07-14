from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable

from app.core.events.event import BaseEvent
from app.core.events.exceptions import (
    EventAlreadyRegisteredError,
    EventNotRegisteredError,
)
from app.core.events.types import EventListener


class EventRegistry:
    """
    Stores listeners for each event type.

    Responsibility:
        - Register listener
        - Unregister listener
        - Retrieve listeners
    """

    def __init__(self) -> None:
        self._listeners: dict[type[BaseEvent], list[EventListener]] = defaultdict(list)

    def register(
        self,
        event_type: type[BaseEvent],
        listener: EventListener,
    ) -> None:
        listeners = self._listeners[event_type]

        if listener in listeners:
            raise EventAlreadyRegisteredError(
                f"{listener.__name__} already registered for "
                f"{event_type.__name__}"
            )

        listeners.append(listener)

    def unregister(
        self,
        event_type: type[BaseEvent],
        listener: EventListener,
    ) -> None:
        listeners = self._listeners.get(event_type)

        if listeners is None or listener not in listeners:
            raise EventNotRegisteredError(
                f"{listener.__name__} is not registered for "
                f"{event_type.__name__}"
            )

        listeners.remove(listener)

        if not listeners:
            del self._listeners[event_type]

    def get(
        self,
        event_type: type[BaseEvent],
    ) -> tuple[EventListener, ...]:
        return tuple(self._listeners.get(event_type, ()))

    def has(
        self,
        event_type: type[BaseEvent],
    ) -> bool:
        return event_type in self._listeners

    def clear(self) -> None:
        self._listeners.clear()

    def registered_events(self) -> tuple[type[BaseEvent], ...]:
        return tuple(self._listeners.keys())

    def registered_listeners(
        self,
        event_type: type[BaseEvent],
    ) -> Iterable[EventListener]:
        return tuple(self._listeners.get(event_type, ()))


__all__ = ["EventRegistry"]
