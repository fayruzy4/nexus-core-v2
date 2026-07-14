from __future__ import annotations

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.core.constants import BACK_BUTTON
from app.modules.habit.controllers.habit_controller import HabitController
from app.modules.habit.dto.habit import HabitCreateDTO
from app.modules.habit.keyboard.categories import category_keyboard
from app.modules.habit.keyboard.custom_days import WEEKDAY_BUTTONS, custom_days_keyboard
from app.modules.habit.keyboard.menu import habit_menu_keyboard
from app.modules.habit.keyboard.schedule import schedule_type_keyboard
from app.modules.habit.states.add_habit import AddHabitStates
from app.modules.habit.texts.buttons import ADD_HABIT, CUSTOM, EVERYDAY, FINISH, OTHER
from app.modules.habit.texts.messages import habit_saved
from app.modules.habit.texts.prompts import (
    ASK_CUSTOM_DAYS,
    ASK_HABIT_CATEGORY,
    ASK_HABIT_CATEGORY_CUSTOM,
    ASK_HABIT_EMOJI,
    ASK_HABIT_NAME,
    ASK_SCHEDULE_TYPE,
)
from app.modules.habit.validators import validate_category, validate_emoji, validate_name, validate_selected_days

router = Router(name='habit-add')


@router.message(F.text == ADD_HABIT)
async def add_habit_start(message: Message, state: FSMContext) -> None:
    await state.set_state(AddHabitStates.name)
    await message.answer(ASK_HABIT_NAME)


@router.message(AddHabitStates.name)
async def add_habit_name(message: Message, state: FSMContext) -> None:
    try:
        name = validate_name(message.text or '')
    except ValueError as exc:
        await message.answer(str(exc))
        return

    await state.update_data(name=name)
    await state.set_state(AddHabitStates.emoji)
    await message.answer(ASK_HABIT_EMOJI)


@router.message(AddHabitStates.emoji)
async def add_habit_emoji(message: Message, state: FSMContext) -> None:
    try:
        emoji = validate_emoji(message.text or '')
    except ValueError as exc:
        await message.answer(str(exc))
        return

    await state.update_data(emoji=emoji)
    await state.set_state(AddHabitStates.category)
    await message.answer(ASK_HABIT_CATEGORY, reply_markup=category_keyboard())


@router.message(AddHabitStates.category)
async def add_habit_category(message: Message, state: FSMContext) -> None:
    text = (message.text or '').strip()
    if text == BACK_BUTTON:
        await state.clear()
        await message.answer('Dibatalkan.', reply_markup=habit_menu_keyboard())
        return

    if text == OTHER:
        await state.set_state(AddHabitStates.category_custom)
        await message.answer(ASK_HABIT_CATEGORY_CUSTOM)
        return

    try:
        category = validate_category(text)
    except ValueError as exc:
        await message.answer(str(exc))
        return

    await state.update_data(category=category)
    await state.set_state(AddHabitStates.schedule_type)
    await message.answer(ASK_SCHEDULE_TYPE, reply_markup=schedule_type_keyboard())


@router.message(AddHabitStates.category_custom)
async def add_habit_category_custom(message: Message, state: FSMContext) -> None:
    if (message.text or '').strip() == BACK_BUTTON:
        await state.set_state(AddHabitStates.category)
        await message.answer(ASK_HABIT_CATEGORY, reply_markup=category_keyboard())
        return

    try:
        category = validate_category(message.text or '')
    except ValueError as exc:
        await message.answer(str(exc))
        return

    await state.update_data(category=category)
    await state.set_state(AddHabitStates.schedule_type)
    await message.answer(ASK_SCHEDULE_TYPE, reply_markup=schedule_type_keyboard())


@router.message(AddHabitStates.schedule_type)
async def add_habit_schedule_type(message: Message, state: FSMContext, habit_controller: HabitController) -> None:
    text = (message.text or '').strip()
    if text == BACK_BUTTON:
        await state.clear()
        await message.answer('Dibatalkan.', reply_markup=habit_menu_keyboard())
        return

    if text == EVERYDAY:
        data = await state.get_data()
        created = await habit_controller.create_habit(
            HabitCreateDTO(
                owner_telegram_id=message.from_user.id,
                name=data['name'],
                emoji=data['emoji'],
                category=data['category'],
                schedule_type='everyday',
                scheduled_days=[1, 2, 3, 4, 5, 6, 7],
            )
        )
        await state.clear()
        await message.answer(habit_saved(created.name), reply_markup=habit_menu_keyboard())
        return

    if text == CUSTOM:
        await state.set_state(AddHabitStates.custom_days)
        await state.update_data(selected_days=[])
        await message.answer(ASK_CUSTOM_DAYS, reply_markup=custom_days_keyboard([]))
        return

    await message.answer(ASK_SCHEDULE_TYPE, reply_markup=schedule_type_keyboard())


@router.message(AddHabitStates.custom_days)
async def add_habit_custom_days(message: Message, state: FSMContext, habit_controller: HabitController) -> None:
    raw_text = (message.text or '').strip()
    data = await state.get_data()
    selected_days = list(data.get('selected_days', []))

    if raw_text == BACK_BUTTON:
        await state.set_state(AddHabitStates.schedule_type)
        await message.answer(ASK_SCHEDULE_TYPE, reply_markup=schedule_type_keyboard())
        return

    if raw_text == FINISH:
        try:
            selected_days = validate_selected_days(selected_days)
        except ValueError as exc:
            await message.answer(str(exc), reply_markup=custom_days_keyboard(selected_days))
            return

        full_data = await state.get_data()
        created = await habit_controller.create_habit(
            HabitCreateDTO(
                owner_telegram_id=message.from_user.id,
                name=full_data['name'],
                emoji=full_data['emoji'],
                category=full_data['category'],
                schedule_type='custom',
                scheduled_days=selected_days,
            )
        )
        await state.clear()
        await message.answer(habit_saved(created.name), reply_markup=habit_menu_keyboard())
        return

    day_map = {day_name: idx for idx, day_name in enumerate(WEEKDAY_BUTTONS, start=1)}
    normalized_text = raw_text.replace('鉁� ', '', 1)
    if normalized_text in day_map:
        day_number = day_map[normalized_text]
        if day_number in selected_days:
            selected_days.remove(day_number)
        else:
            selected_days.append(day_number)
        await state.update_data(selected_days=selected_days)
        await message.answer(ASK_CUSTOM_DAYS, reply_markup=custom_days_keyboard(sorted(selected_days)))
        return

    await message.answer(ASK_CUSTOM_DAYS, reply_markup=custom_days_keyboard(selected_days))
