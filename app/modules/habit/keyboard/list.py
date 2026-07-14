from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from app.core.constants import BACK_BUTTON
from app.modules.habit.texts.buttons import CHECKIN, UNDO, DELETE_HABIT


def habit_list_keyboard(habit_buttons: list[str]) -> ReplyKeyboardMarkup:
    rows = [[KeyboardButton(text=item)] for item in habit_buttons]
    rows.append([KeyboardButton(text=BACK_BUTTON)])
    return ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True, is_persistent=True)


def habit_detail_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=CHECKIN), KeyboardButton(text=UNDO)],
            [KeyboardButton(text=DELETE_HABIT)],
            [KeyboardButton(text=BACK_BUTTON)],
        ],
        resize_keyboard=True,
        is_persistent=True,
    )
