from __future__ import annotations

from datetime import date

import asyncpg

from app.modules.habit.repositories import queries


class HabitRepository:
    def __init__(self, pool: asyncpg.Pool) -> None:
        self.pool = pool

    async def create_habit(
        self,
        owner_telegram_id: int,
        name: str,
        emoji: str,
        category: str,
        schedule_type: str,
        scheduled_days: list[int],
    ) -> asyncpg.Record:
        async with self.pool.acquire() as conn:
            return await conn.fetchrow(
                queries.CREATE_HABIT,
                owner_telegram_id,
                name,
                emoji,
                category,
                schedule_type,
                scheduled_days,
            )

    async def list_habits(self, owner_telegram_id: int) -> list[asyncpg.Record]:
        async with self.pool.acquire() as conn:
            return list(await conn.fetch(queries.LIST_HABITS_BY_OWNER, owner_telegram_id))

    async def list_habits_with_ids(self, owner_telegram_id: int) -> list[asyncpg.Record]:
        async with self.pool.acquire() as conn:
            return list(await conn.fetch(queries.LIST_HABITS_WITH_IDS_BY_OWNER, owner_telegram_id))

    async def get_habit(self, habit_id: int, owner_telegram_id: int) -> asyncpg.Record | None:
        async with self.pool.acquire() as conn:
            return await conn.fetchrow(queries.GET_HABIT_BY_ID, habit_id, owner_telegram_id)

    async def delete_habit(self, habit_id: int, owner_telegram_id: int) -> asyncpg.Record | None:
        async with self.pool.acquire() as conn:
            return await conn.fetchrow(queries.DELETE_HABIT, habit_id, owner_telegram_id)

    async def insert_checkin(self, habit_id: int, checkin_date: date) -> asyncpg.Record:
        async with self.pool.acquire() as conn:
            return await conn.fetchrow(queries.INSERT_CHECKIN, habit_id, checkin_date)

    async def delete_checkin(self, habit_id: int, checkin_date: date) -> asyncpg.Record | None:
        async with self.pool.acquire() as conn:
            return await conn.fetchrow(queries.DELETE_CHECKIN, habit_id, checkin_date)

    async def get_checkin_by_date(self, habit_id: int, checkin_date: date) -> asyncpg.Record | None:
        async with self.pool.acquire() as conn:
            return await conn.fetchrow(queries.GET_CHECKIN_BY_DATE, habit_id, checkin_date)

    async def list_checkins_by_habit(self, habit_id: int) -> list[date]:
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(queries.LIST_CHECKINS_BY_HABIT, habit_id)
            return [row['checkin_date'] for row in rows]

    async def list_checkins_by_owner_range(self, owner_telegram_id: int, start_date: date, end_date: date) -> list[asyncpg.Record]:
        async with self.pool.acquire() as conn:
            return list(await conn.fetch(queries.LIST_CHECKINS_BY_OWNER_RANGE, owner_telegram_id, start_date, end_date))

    async def update_habit_stats(
        self,
        habit_id: int,
        owner_telegram_id: int,
        current_streak: int,
        longest_streak: int,
        total_completion: int,
        total_missed: int,
    ) -> asyncpg.Record | None:
        async with self.pool.acquire() as conn:
            return await conn.fetchrow(
                queries.UPDATE_HABIT_STATS,
                current_streak,
                longest_streak,
                total_completion,
                total_missed,
                habit_id,
                owner_telegram_id,
            )
