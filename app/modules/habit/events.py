from __future__ import annotations

from app.core.events.event import BaseEvent


class HabitCreatedEvent(BaseEvent):
    def __init__(
        self,
        *,
        owner_telegram_id: int,
        habit_id: int,
        name: str,
        emoji: str,
        category: str,
        schedule_type: str,
        scheduled_days: list[int],
    ) -> None:
        super().__init__(
            event_name='HabitCreatedEvent',
            payload={
                'owner_telegram_id': owner_telegram_id,
                'habit_id': habit_id,
                'name': name,
                'emoji': emoji,
                'category': category,
                'schedule_type': schedule_type,
                'scheduled_days': list(scheduled_days),
            },
        )


class HabitCompletedEvent(BaseEvent):
    def __init__(
        self,
        *,
        owner_telegram_id: int,
        habit_id: int,
        name: str,
        current_streak: int,
        longest_streak: int,
        total_completion: int,
        total_missed: int,
    ) -> None:
        super().__init__(
            event_name='HabitCompletedEvent',
            payload={
                'owner_telegram_id': owner_telegram_id,
                'habit_id': habit_id,
                'name': name,
                'current_streak': current_streak,
                'longest_streak': longest_streak,
                'total_completion': total_completion,
                'total_missed': total_missed,
            },
        )


class HabitUncheckedEvent(BaseEvent):
    def __init__(
        self,
        *,
        owner_telegram_id: int,
        habit_id: int,
        name: str,
        current_streak: int,
        longest_streak: int,
        total_completion: int,
        total_missed: int,
    ) -> None:
        super().__init__(
            event_name='HabitUncheckedEvent',
            payload={
                'owner_telegram_id': owner_telegram_id,
                'habit_id': habit_id,
                'name': name,
                'current_streak': current_streak,
                'longest_streak': longest_streak,
                'total_completion': total_completion,
                'total_missed': total_missed,
            },
        )


class HabitDeletedEvent(BaseEvent):
    def __init__(
        self,
        *,
        owner_telegram_id: int,
        habit_id: int,
        name: str,
        emoji: str,
        category: str,
    ) -> None:
        super().__init__(
            event_name='HabitDeletedEvent',
            payload={
                'owner_telegram_id': owner_telegram_id,
                'habit_id': habit_id,
                'name': name,
                'emoji': emoji,
                'category': category,
            },
        )


class HabitStatsUpdatedEvent(BaseEvent):
    def __init__(
        self,
        *,
        owner_telegram_id: int,
        habit_id: int,
        current_streak: int,
        longest_streak: int,
        total_completion: int,
        total_missed: int,
    ) -> None:
        super().__init__(
            event_name='HabitStatsUpdatedEvent',
            payload={
                'owner_telegram_id': owner_telegram_id,
                'habit_id': habit_id,
                'current_streak': current_streak,
                'longest_streak': longest_streak,
                'total_completion': total_completion,
                'total_missed': total_missed,
            },
        )
