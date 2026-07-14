from __future__ import annotations

from app.modules.habit.dto.habit import HabitDTO


def habit_from_record(record) -> HabitDTO:
    return HabitDTO(
        id=record['id'],
        owner_telegram_id=record['owner_telegram_id'],
        name=record['name'],
        emoji=record['emoji'],
        category=record['category'],
        schedule_type=record['schedule_type'],
        scheduled_days=list(record['scheduled_days'] or []),
        current_streak=record['current_streak'],
        longest_streak=record['longest_streak'],
        total_completion=record['total_completion'],
        total_missed=record['total_missed'],
        created_at=record['created_at'],
    )
