from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from typing import Sequence


@dataclass(slots=True)
class HabitDTO:
    id: int
    owner_telegram_id: int
    name: str
    emoji: str
    category: str
    schedule_type: str
    scheduled_days: list[int]
    current_streak: int
    longest_streak: int
    total_completion: int
    total_missed: int
    created_at: datetime


@dataclass(slots=True)
class HabitCreateDTO:
    owner_telegram_id: int
    name: str
    emoji: str
    category: str
    schedule_type: str
    scheduled_days: list[int]


@dataclass(slots=True)
class EvaluationDTO:
    period_label: str
    start_date: date
    end_date: date
    scheduled_days: int
    completed_days: int
    missed_days: int
    completion_rate: float
    streak_habits: int
    chart_bytes: bytes


@dataclass(slots=True)
class HabitStatsSnapshot:
    current_streak: int
    longest_streak: int
    total_completion: int
    total_missed: int
