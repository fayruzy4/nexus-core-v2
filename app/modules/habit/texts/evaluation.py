from __future__ import annotations

from app.modules.habit.dto.habit import EvaluationDTO


def evaluation_text(result: EvaluationDTO) -> str:
    return (
        f'Evaluasi Habit\n'
        f'Periode: {result.period_label}\n'
        f'Range: {result.start_date.isoformat()} s/d {result.end_date.isoformat()}\n\n'
        f'Scheduled Days: {result.scheduled_days}\n'
        f'Completed: {result.completed_days}\n'
        f'Missed: {result.missed_days}\n'
        f'Completion Rate: {result.completion_rate:.2f}%\n'
        f'Habit yang masih punya streak: {result.streak_habits}'
    )
