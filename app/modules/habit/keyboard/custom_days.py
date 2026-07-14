from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from app.core.constants import BACK_BUTTON
from app.modules.habit.texts.buttons import FINISH

WEEKDAY_BUTTONS = [
    'Senin',
    'Selasa',
    'Rabu',
    'Kamis',
    'Jumat',
    'Sabtu',
    'Minggu',
]


def custom_days_keyboard(selected_days: list[int]) -> ReplyKeyboardMarkup:
    rows = []
    for idx, day_name in enumerate(WEEKDAY_BUTTONS, start=1):
        prefix = '✅ ' if idx in selected_days else ''
        rows.append([KeyboardButton(text=f'{prefix}{day_name}')])
    rows.append([KeyboardButton(text=FINISH)])
    rows.append([KeyboardButton(text=BACK_BUTTON)])
    return ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True, is_persistent=True)
