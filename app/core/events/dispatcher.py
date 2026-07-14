from __future__ import annotations

import asyncio
import logging

from app.core.events.event import BaseEvent
from app.core.events.types import EventListener

logger = logging.getLogger(__name__)


class EventDispatcher:
    """
    Dispatches events to listeners.

    Responsibility:
        - Fire & Forget dispatch
        - Isolate listener failures
        - Never propagate listener exceptions
    """

    async def dispatch(
        self,
        event: BaseEvent,
        listeners: tuple[EventListener, ...],
    ) -> None:
        if not listeners:
            return

        for listener in listeners:
            asyncio.create_task(
                self._execute_listener(
                    listener=listener,
                    event=event,
                )
            )

    async def _execute_listener(
        self,
        *,
        listener: EventListener,
        event: BaseEvent,
    ) -> None:
        try:
            await listener(event)

        except asyncio.CancelledError:
            raise

        except Exception:
            logger.exception(
                "Event listener '%s' failed while handling '%s'",
                listener.__name__,
                event.event_name,
            )


__all__ = [
    "EventDispatcher",
]
