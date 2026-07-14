from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from datetime import date, timedelta

from app.modules.habit.dto.habit import EvaluationDTO, HabitCreateDTO, HabitDTO, HabitStatsSnapshot
from app.modules.habit.mappers import habit_from_record
from app.modules.habit.repositories.habit_repository import HabitRepository
from app.modules.habit.utils.chart import build_pie_chart
from app.modules.habit.utils.dates import PERIOD_MAP, is_scheduled_day, scheduled_days_between, today_local
from app.core.events.publisher import publish
from app.modules.habit.events import (
    HabitCompletedEvent,
    HabitCreatedEvent,
    HabitDeletedEvent,
    HabitStatsUpdatedEvent,
    HabitUncheckedEvent,
)


@dataclass(slots=True)
class EvaluationPreparedData:
    summary: EvaluationDTO
    habits: list[HabitDTO]


class HabitService:
    def __init__(self, repository: HabitRepository) -> None:
        self.repository = repository

    async def create_habit(self, dto: HabitCreateDTO) -> HabitDTO:
        record = await self.repository.create_habit(
            dto.owner_telegram_id,
            dto.name,
            dto.emoji,
            dto.category,
            dto.schedule_type,
            dto.scheduled_days,
        )
        habit = habit_from_record(record)
        await self.recalculate_stats(habit.id, habit.owner_telegram_id)
    refreshed = await self.repository.get_habit(
    habit.id,
    habit.owner_telegram_id,
)
    refreshed_habit = habit_from_record(refreshed)

    await publish(
            HabitCreatedEvent(
                    owner_telegram_id=refreshed_habit.owner_telegram_id,
                    habit_id=refreshed_habit.id,
                    name=refreshed_habit.name,
                    emoji=refreshed_habit.emoji,
                    category=refreshed_habit.category,
                    schedule_type=refreshed_habit.schedule_type,
                    scheduled_days=refreshed_habit.scheduled_days,
            )
    )
    return refreshed_habit
    async def list_habits(self, owner_telegram_id: int) -> list[HabitDTO]:
        rows = await self.repository.list_habits(owner_telegram_id)
        return [habit_from_record(row) for row in rows]

    async def list_habits_with_ids(self, owner_telegram_id: int) -> list[HabitDTO]:
        rows = await self.repository.list_habits_with_ids(owner_telegram_id)
        return [habit_from_record(row) for row in rows]

    async def get_habit(self, habit_id: int, owner_telegram_id: int) -> HabitDTO | None:
        record = await self.repository.get_habit(habit_id, owner_telegram_id)
        if record is None:
            return None
        return habit_from_record(record)

    async def delete_habit(self, habit_id: int, owner_telegram_id: int) -> HabitDTO | None:
        habit = await self.get_habit(habit_id, owner_telegram_id)
        if habit is None:
            return None
        await self.repository.delete_habit(habit_id, owner_telegram_id)

        await publish(
            HabitDeletedEvent(
                    owner_telegram_id=habit.owner_telegram_id,
                    habit_id=habit.id,
                    name=habit.name,
                    emoji=habit.emoji,
                    category=habit.category,
            )
        )

        return habit

    async def check_in_today(self, habit_id: int, owner_telegram_id: int) -> tuple[HabitDTO | None, str | None]:
        habit = await self.get_habit(habit_id, owner_telegram_id)
        if habit is None:
            return None, 'habit_not_found'

        today = today_local()
        if not is_scheduled_day(habit.schedule_type, habit.scheduled_days, today):
            return habit, 'not_due_today'

        already = await self.repository.get_checkin_by_date(habit_id, today)
        if already is not None:
            return habit, 'already_checked'

        await self.repository.insert_checkin(habit_id, today)
                await self.recalculate_stats(habit_id, owner_telegram_id)

        refreshed = await self.repository.get_habit(
            habit_id,
            owner_telegram_id,
        )
        refreshed_habit = habit_from_record(refreshed)

        await publish(
            HabitCompletedEvent(
                owner_telegram_id=refreshed_habit.owner_telegram_id,
                habit_id=refreshed_habit.id,
                name=refreshed_habit.name,
                current_streak=refreshed_habit.current_streak,
                longest_streak=refreshed_habit.longest_streak,
                total_completion=refreshed_habit.total_completion,
                total_missed=refreshed_habit.total_missed,
            )
        )

        return refreshed_habit, None

    async def undo_today_checkin(self, habit_id: int, owner_telegram_id: int) -> tuple[HabitDTO | None, str | None]:
        habit = await self.get_habit(habit_id, owner_telegram_id)
        if habit is None:
            return None, 'habit_not_found'

        today = today_local()
        removed = await self.repository.delete_checkin(habit_id, today)
        if removed is None:
            return habit, 'no_today_checkin'

               await self.recalculate_stats(habit_id, owner_telegram_id)

        refreshed = await self.repository.get_habit(
            habit_id,
            owner_telegram_id,
        )
        refreshed_habit = habit_from_record(refreshed)

        await publish(
            HabitUncheckedEvent(
                owner_telegram_id=refreshed_habit.owner_telegram_id,
                habit_id=refreshed_habit.id,
                name=refreshed_habit.name,
                current_streak=refreshed_habit.current_streak,
                longest_streak=refreshed_habit.longest_streak,
                total_completion=refreshed_habit.total_completion,
                total_missed=refreshed_habit.total_missed,
            )
        )

        return refreshed_habit, None

    async def recalculate_stats(self, habit_id: int, owner_telegram_id: int) -> HabitStatsSnapshot:
        habit = await self.get_habit(habit_id, owner_telegram_id)
        if habit is None:
            raise RuntimeError('Habit tidak ditemukan saat menghitung statistik.')

        checkins = await self.repository.list_checkins_by_habit(habit_id)
        checkin_set = set(checkins)
        start_date = habit.created_at.date()
        end_date = today_local()

        current_run = 0
        longest_run = 0
        consecutive_missed = 0
        total_completion = len(checkins)
        total_missed = 0

        for current_day in scheduled_days_between(habit.schedule_type, habit.scheduled_days, start_date, end_date):
            if current_day in checkin_set:
                if current_run == 0 or consecutive_missed >= 3:
                    current_run = 1
                else:
                    current_run += 1
                longest_run = max(longest_run, current_run)
                consecutive_missed = 0
            else:
                total_missed += 1
                consecutive_missed += 1
                if consecutive_missed >= 3:
                    current_run = 0

        await self.repository.update_habit_stats(
            habit_id=habit_id,
            owner_telegram_id=owner_telegram_id,
            current_streak=current_run,
            longest_streak=max(longest_run, current_run),
            total_completion=total_completion,
            total_missed=total_missed,
        )

        snapshot = HabitStatsSnapshot(
            current_streak=current_run,
            longest_streak=max(longest_run, current_run),
            total_completion=total_completion,
            total_missed=total_missed,
        )

        await publish(
            HabitStatsUpdatedEvent(
                owner_telegram_id=owner_telegram_id,
                habit_id=habit_id,
                current_streak=snapshot.current_streak,
                longest_streak=snapshot.longest_streak,
                total_completion=snapshot.total_completion,
                total_missed=snapshot.total_missed,
            )
        )

        return snapshot
    async def build_evaluation(self, owner_telegram_id: int, period_label: str) -> EvaluationDTO:
        days = PERIOD_MAP[period_label]
        end_date = today_local()
        start_date = end_date - timedelta(days=days - 1)

        habits = await self.list_habits(owner_telegram_id)
        total_scheduled = 0
        total_completed = 0
        total_missed = 0
        active_streak_habits = 0

        for habit in habits:
            scheduled_days = scheduled_days_between(
                habit.schedule_type,
                habit.scheduled_days,
                max(start_date, habit.created_at.date()),
                end_date,
            )
            checkins = await self.repository.list_checkins_by_habit(habit.id)
            checkin_set = {day for day in checkins if start_date <= day <= end_date}
            scheduled_count = len(scheduled_days)
            completed_count = sum(1 for day in scheduled_days if day in checkin_set)
            missed_count = scheduled_count - completed_count
            total_scheduled += scheduled_count
            total_completed += completed_count
            total_missed += missed_count
            if habit.current_streak > 0:
                active_streak_habits += 1

        completion_rate = (total_completed / total_scheduled * 100.0) if total_scheduled else 0.0
        chart_bytes = build_pie_chart(
            labels=['Completed', 'Missed'],
            values=[total_completed or 1, total_missed or 1],
            title=f'Habit Completion ({period_label})',
        )

        return EvaluationDTO(
            period_label=period_label,
            start_date=start_date,
            end_date=end_date,
            scheduled_days=total_scheduled,
            completed_days=total_completed,
            missed_days=total_missed,
            completion_rate=completion_rate,
            streak_habits=active_streak_habits,
            chart_bytes=chart_bytes,
        )
