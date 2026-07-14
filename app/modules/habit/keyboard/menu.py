from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from app.core.constants import BACK_BUTTON
from app.modules.habit.texts.buttons import ADD_HABIT, LIST_HABIT, EVALUATION, DELETE_HABIT


def habit_menu_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=ADD_HABIT), KeyboardButton(text=LIST_HABIT)],
            [KeyboardButton(text=EVALUATION), KeyboardButton(text=DELETE_HABIT)],
            [KeyboardButton(text=BACK_BUTTON)],
        ],
        resize_keyboard=True,
        is_persistent=True,
        input_field_placeholder='Pilih aksi habit',
    )
