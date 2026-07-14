from aiogram import Router

from app.modules.habit.handlers.add_habit import router as add_router
from app.modules.habit.handlers.evaluation import router as evaluation_router
from app.modules.habit.handlers.habit_item import router as item_router
from app.modules.habit.handlers.navigation import router as navigation_router


def build_habit_router() -> Router:
    router = Router(name='habit-root')
    router.include_router(navigation_router)
    router.include_router(add_router)
    router.include_router(item_router)
    router.include_router(evaluation_router)
    return router
