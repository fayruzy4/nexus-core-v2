from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from app.core.constants import BACK_BUTTON
from app.modules.habit.texts.buttons import CUSTOM, EVERYDAY


def schedule_type_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=EVERYDAY)],
            [KeyboardButton(text=CUSTOM)],
            [KeyboardButton(text=BACK_BUTTON)],
        ],
        resize_keyboard=True,
        is_persistent=True,
    )
