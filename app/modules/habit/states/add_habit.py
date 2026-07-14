from aiogram.fsm.state import State, StatesGroup


class AddHabitStates(StatesGroup):
    name = State()
    emoji = State()
    category = State()
    category_custom = State()
    schedule_type = State()
    custom_days = State()
