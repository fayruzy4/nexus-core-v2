from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from app.core.constants import PROJECT_MAIN_MENU_BUTTON


def main_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=PROJECT_MAIN_MENU_BUTTON)]],
        resize_keyboard=True,
        is_persistent=True,
        input_field_placeholder='Pilih menu',
    )
