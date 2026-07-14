from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from app.core.constants import BACK_BUTTON
from app.modules.habit.texts.buttons import OTHER

CATEGORY_ITEMS = [
    'Kesehatan',
    'Belajar',
    'Ibadah',
    'Olahraga',
    'Produktivitas',
    'Finansial',
    'Karier',
    'Rumah',
    OTHER,
]


def category_keyboard() -> ReplyKeyboardMarkup:
    rows = []
    for item in CATEGORY_ITEMS:
        rows.append([KeyboardButton(text=item)])
    rows.append([KeyboardButton(text=BACK_BUTTON)])
    return ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True, is_persistent=True)
