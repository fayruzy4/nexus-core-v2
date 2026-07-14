from __future__ import annotations

import re

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
import logging

logger = logging.getLogger(__name__)

from app.core.constants import NO_BUTTON, YES_BUTTON
from app.modules.habit.controllers.habit_controller import HabitController
from app.modules.habit.keyboard.delete import delete_confirm_keyboard
from app.modules.habit.keyboard.menu import habit_menu_keyboard
from app.modules.habit.keyboard.list import habit_detail_keyboard, habit_list_keyboard
from app.modules.habit.texts.buttons import CHECKIN, DELETE_HABIT, LIST_HABIT, UNDO
from app.modules.habit.texts.detail import habit_detail_text
from app.modules.habit.texts.messages import (
    already_checked_in,
    checkin_success,
    habit_deleted,
    habit_not_found,
    no_habits,
    no_today_checkin,
    not_due_today,
    undo_success,
)

router = Router(name='habit-item')
HABIT_ID_PATTERN = re.compile(r'^#(?P<id>\d+)\s+')


@router.message(F.text == LIST_HABIT)
async def show_habit_list(message: Message, state: FSMContext, habit_controller: HabitController) -> None:
    habits = await habit_controller.list_habits_with_ids(message.from_user.id)
    if not habits:
        await message.answer(no_habits())
        return

    buttons = [f'#{habit.id} {habit.emoji} {habit.name}' for habit in habits]
    await state.update_data(current_habit_ids=[habit.id for habit in habits])
    await message.answer('Pilih habit yang ingin dibuka.', reply_markup=habit_list_keyboard(buttons))


@router.message(F.text.regexp(r'^#\d+\s+'))
async def open_habit_detail_by_button(message: Message, state: FSMContext, habit_controller: HabitController) -> None:
    match = HABIT_ID_PATTERN.match(message.text or '')
    if not match:
        await message.answer(habit_not_found())
        return

    habit_id = int(match.group('id'))
    habit = await habit_controller.get_habit(habit_id, message.from_user.id)
    if habit is None:
        await message.answer(habit_not_found())
        return

    await state.update_data(active_habit_id=habit.id)
    await message.answer(habit_detail_text(habit), reply_markup=habit_detail_keyboard())


@router.message(F.text == CHECKIN)
async def habit_checkin(message: Message, state: FSMContext, habit_controller: HabitController) -> None:
    data = await state.get_data()
    habit_id = data.get('active_habit_id')
    if not habit_id:
        await message.answer(habit_not_found())
        return

    habit, error = await habit_controller.check_in_today(int(habit_id), message.from_user.id)
    if error == 'habit_not_found' or habit is None:
        await message.answer(habit_not_found())
        return
    if error == 'not_due_today':
        await message.answer(not_due_today(habit.name))
        return
    if error == 'already_checked':
        await message.answer(already_checked_in(habit.name))
        return

    await message.answer(checkin_success(habit.name))
    await message.answer(habit_detail_text(habit), reply_markup=habit_detail_keyboard())


@router.message()
async def habit_undo(message: Message, state: FSMContext, habit_controller: HabitController) -> None:
    logger.info("TEXT=%r", message.text)

    if message.text != UNDO:
        return

    data = await state.get_data()
    logger.info("UNDO STATE=%s", data)
    logger.info("UNDO STATE: %s", data)
    habit_id = data.get('active_habit_id')
    if not habit_id:
        await message.answer(habit_not_found())
        return

    habit, error = await habit_controller.undo_today_checkin(int(habit_id), message.from_user.id)
    if error == 'habit_not_found' or habit is None:
        await message.answer(habit_not_found())
        return
    if error == 'no_today_checkin':
        await message.answer(no_today_checkin(habit.name))
        return

    await message.answer(undo_success(habit.name))
    await message.answer(habit_detail_text(habit), reply_markup=habit_detail_keyboard())


@router.message(F.text == DELETE_HABIT)
async def ask_delete(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    habit_id = data.get('active_habit_id')
    if not habit_id:
        await message.answer(habit_not_found())
        return

    await state.update_data(delete_target_id=int(habit_id))
    await message.answer('Hapus habit ini? Semua riwayat juga ikut terhapus.', reply_markup=delete_confirm_keyboard())


@router.message(F.text == YES_BUTTON)
async def confirm_delete(message: Message, state: FSMContext, habit_controller: HabitController) -> None:
    data = await state.get_data()
    habit_id = data.get('delete_target_id')
    if not habit_id:
        return

    deleted = await habit_controller.delete_habit(int(habit_id), message.from_user.id)
    if deleted is None:
        await message.answer(habit_not_found())
        return

    await state.clear()
    await message.answer(habit_deleted(deleted.name), reply_markup=habit_menu_keyboard())


@router.message(F.text == NO_BUTTON)
async def cancel_delete(message: Message, state: FSMContext, habit_controller: HabitController) -> None:
    data = await state.get_data()
    habit_id = data.get('active_habit_id')
    if not habit_id:
        return

    habit = await habit_controller.get_habit(int(habit_id), message.from_user.id)
    if habit is None:
        await message.answer(habit_not_found())
        return

    await state.update_data(delete_target_id=None)
    await message.answer(habit_detail_text(habit), reply_markup=habit_detail_keyboard())
