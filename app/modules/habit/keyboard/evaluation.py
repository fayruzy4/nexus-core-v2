from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from app.core.constants import BACK_BUTTON

PERIOD_BUTTONS = [
    '14 Hari',
    '30 Hari',
    '90 Hari',
    '180 Hari',
    '1 Tahun',
]


def evaluation_keyboard() -> ReplyKeyboardMarkup:
    rows = [[KeyboardButton(text=item)] for item in PERIOD_BUTTONS]
    rows.append([KeyboardButton(text=BACK_BUTTON)])
    return ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True, is_persistent=True)
