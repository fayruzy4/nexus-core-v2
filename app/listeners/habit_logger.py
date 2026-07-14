from __future__ import annotations

import logging

from app.core.events.event import BaseEvent

logger = logging.getLogger(__name__)


async def log_event(event: BaseEvent) -> None:
    logger.info(
        "[EVENT] %s -> %s",
        event.event_name,
        event.payload,
    )
