from __future__ import annotations

from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message


ACCESS_DENIED_TEXT = 'Access denied. This is a private bot and is only configured to respond to its authorized owner.'


class OwnerOnlyMiddleware(BaseMiddleware):
    def __init__(self, owner_telegram_id: int) -> None:
        self.owner_telegram_id = owner_telegram_id

    async def __call__(
        self,
        handler: Callable[[Any, dict[str, Any]], Awaitable[Any]],
        event: Any,
        data: dict[str, Any],
    ) -> Any:
        user = getattr(event, 'from_user', None)
        if user is None:
            return await handler(event, data)

        if user.id != self.owner_telegram_id:
            if isinstance(event, Message):
                await event.answer(ACCESS_DENIED_TEXT)
            elif isinstance(event, CallbackQuery) and event.message is not None:
                await event.message.answer(ACCESS_DENIED_TEXT)
            return None

        return await handler(event, data)
