from __future__ import annotations

from app.core.events.subscriber import subscribe
from app.listeners.habit_logger import log_event
from app.modules.habit.events import (
    HabitCompletedEvent,
    HabitCreatedEvent,
    HabitDeletedEvent,
    HabitStatsUpdatedEvent,
    HabitUncheckedEvent,
)


def register_listeners() -> None:
    subscribe(HabitCreatedEvent, log_event)
    subscribe(HabitCompletedEvent, log_event)
    subscribe(HabitUncheckedEvent, log_event)
    subscribe(HabitDeletedEvent, log_event)
    subscribe(HabitStatsUpdatedEvent, log_event)
