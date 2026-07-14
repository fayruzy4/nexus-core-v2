from __future__ import annotations

from app.core.events.dispatcher import EventDispatcher
from app.core.events.event import BaseEvent
from app.core.events.registry import EventRegistry
from app.core.events.types import EventListener


class EventBus:
    """
    Internal Event Bus.

    Responsibilities:
        - Register listener
        - Unregister listener
        - Publish event

    Does NOT:
        - Know modules
        - Execute business logic
        - Store events
    """

    _instance: "EventBus | None" = None

    def __new__(cls) -> "EventBus":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._registry = EventRegistry()
            cls._instance._dispatcher = EventDispatcher()

        return cls._instance

    async def publish(self, event: BaseEvent) -> None:
        listeners = self._registry.get(type(event))

        await self._dispatcher.dispatch(
            event=event,
            listeners=listeners,
        )

    def subscribe(
        self,
        event_type: type[BaseEvent],
        listener: EventListener,
    ) -> None:
        self._registry.register(
            event_type=event_type,
            listener=listener,
        )

    def unsubscribe(
        self,
        event_type: type[BaseEvent],
        listener: EventListener,
    ) -> None:
        self._registry.unregister(
            event_type=event_type,
            listener=listener,
        )

    def clear(self) -> None:
        self._registry.clear()


event_bus = EventBus()

__all__ = [
    "EventBus",
    "event_bus",
]
