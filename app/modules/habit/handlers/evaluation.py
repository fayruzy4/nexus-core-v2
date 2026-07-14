from __future__ import annotations

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import BufferedInputFile, Message

from app.modules.habit.controllers.habit_controller import HabitController
from app.modules.habit.keyboard.evaluation import evaluation_keyboard
from app.modules.habit.texts.buttons import EVALUATION
from app.modules.habit.texts.evaluation import evaluation_text
from app.modules.habit.utils.dates import PERIOD_MAP

router = Router(name='habit-evaluation')


@router.message(F.text == EVALUATION)
async def open_evaluation(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer('Pilih periode evaluasi.', reply_markup=evaluation_keyboard())


@router.message(F.text.in_(list(PERIOD_MAP.keys())))
async def show_evaluation(message: Message, habit_controller: HabitController) -> None:
    result = await habit_controller.build_evaluation(message.from_user.id, message.text or '14 Hari')
    await message.answer(evaluation_text(result))
    chart = BufferedInputFile(result.chart_bytes, filename='habit_evaluation.png')
    await message.answer_photo(chart, caption=f'Pie chart: {result.period_label}')
