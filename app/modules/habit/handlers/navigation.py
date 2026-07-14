from __future__ import annotations

from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.core.constants import BACK_BUTTON, PROJECT_MAIN_MENU_BUTTON
from app.modules.habit.keyboard.main import main_keyboard
from app.modules.habit.keyboard.menu import habit_menu_keyboard
from app.modules.habit.texts.menu import HABIT_WELCOME, MAIN_WELCOME

router = Router(name='habit-navigation')


@router.message(CommandStart())
async def start_handler(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(MAIN_WELCOME, reply_markup=main_keyboard())


@router.message(F.text == PROJECT_MAIN_MENU_BUTTON)
async def open_habit_matrix(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(HABIT_WELCOME, reply_markup=habit_menu_keyboard())


@router.message(F.text == BACK_BUTTON)
async def back_handler(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(MAIN_WELCOME, reply_markup=main_keyboard())
