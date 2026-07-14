from __future__ import annotations

from app.modules.habit.dto.habit import HabitDTO
from app.modules.habit.utils.dates import format_day_list


def habit_detail_text(habit: HabitDTO) -> str:
    schedule = 'Setiap Hari' if habit.schedule_type == 'everyday' else f'Kustom: {format_day_list(habit.scheduled_days)}'
    return (
        f'{habit.emoji} {habit.name}\n\n'
        f'Kategori: {habit.category}\n'
        f'Jadwal: {schedule}\n\n'
        f'Current Streak: {habit.current_streak}\n'
        f'Longest Streak: {habit.longest_streak}\n'
        f'Total Completion: {habit.total_completion}\n'
        f'Total Missed: {habit.total_missed}'
    )
