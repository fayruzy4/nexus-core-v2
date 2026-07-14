from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from app.core.constants import NO_BUTTON, YES_BUTTON, BACK_BUTTON


def delete_confirm_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=YES_BUTTON), KeyboardButton(text=NO_BUTTON)],
            [KeyboardButton(text=BACK_BUTTON)],
        ],
        resize_keyboard=True,
        is_persistent=True,
    )
