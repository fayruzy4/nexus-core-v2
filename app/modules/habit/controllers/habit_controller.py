from __future__ import annotations

from app.modules.habit.dto.habit import EvaluationDTO, HabitCreateDTO, HabitDTO, HabitStatsSnapshot
from app.modules.habit.services.habit_service import HabitService


class HabitController:
    def __init__(self, service: HabitService) -> None:
        self.service = service

    async def create_habit(self, dto: HabitCreateDTO) -> HabitDTO:
        return await self.service.create_habit(dto)

    async def list_habits(self, owner_telegram_id: int) -> list[HabitDTO]:
        return await self.service.list_habits(owner_telegram_id)

    async def list_habits_with_ids(self, owner_telegram_id: int) -> list[HabitDTO]:
        return await self.service.list_habits_with_ids(owner_telegram_id)

    async def get_habit(self, habit_id: int, owner_telegram_id: int) -> HabitDTO | None:
        return await self.service.get_habit(habit_id, owner_telegram_id)

    async def delete_habit(self, habit_id: int, owner_telegram_id: int) -> HabitDTO | None:
        return await self.service.delete_habit(habit_id, owner_telegram_id)

    async def check_in_today(self, habit_id: int, owner_telegram_id: int):
        return await self.service.check_in_today(habit_id, owner_telegram_id)

    async def undo_today_checkin(self, habit_id: int, owner_telegram_id: int):
        return await self.service.undo_today_checkin(habit_id, owner_telegram_id)

    async def recalculate_stats(self, habit_id: int, owner_telegram_id: int) -> HabitStatsSnapshot:
        return await self.service.recalculate_stats(habit_id, owner_telegram_id)

    async def build_evaluation(self, owner_telegram_id: int, period_label: str) -> EvaluationDTO:
        return await self.service.build_evaluation(owner_telegram_id, period_label)
