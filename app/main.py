from __future__ import annotations

import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from app.core.config import load_settings
from app.core.db import DatabasePool
from app.core.logging_config import configure_logging
from app.core.middleware import OwnerOnlyMiddleware
from app.modules.habit.controllers.habit_controller import HabitController
from app.modules.habit.repositories.habit_repository import HabitRepository
from app.modules.habit.router import build_habit_router
from app.modules.habit.services.habit_service import HabitService
from app.listeners import register_listeners

async def main() -> None:
    settings = load_settings()
    configure_logging(settings.log_level)

    pool = await DatabasePool.init(settings.database_dsn)
    repository = HabitRepository(pool)
    service = HabitService(repository)
    controller = HabitController(service)

    bot = Bot(token=settings.bot_token)
    dp = Dispatcher(storage=MemoryStorage(), habit_controller=controller)
    dp.update.middleware(OwnerOnlyMiddleware(settings.owner_telegram_id))
    dp.include_router(build_habit_router())

    try:
        register_listeners()
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
        await DatabasePool.close()


if __name__ == '__main__':
    asyncio.run(main())
