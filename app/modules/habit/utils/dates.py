from __future__ import annotations

import os
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

DAY_NAME_TO_ISO = {
    'Senin': 1,
    'Selasa': 2,
    'Rabu': 3,
    'Kamis': 4,
    'Jumat': 5,
    'Sabtu': 6,
    'Minggu': 7,
}

ISO_TO_DAY_NAME = {value: key for key, value in DAY_NAME_TO_ISO.items()}

PERIOD_MAP = {
    '14 Hari': 14,
    '30 Hari': 30,
    '90 Hari': 90,
    '180 Hari': 180,
    '1 Tahun': 365,
}


def _local_tz() -> ZoneInfo:
    return ZoneInfo(os.getenv('TZ', 'Asia/Jakarta'))


def today_local() -> date:
    return datetime.now(_local_tz()).date()


def date_range(start: date, end: date) -> list[date]:
    days: list[date] = []
    current = start
    while current <= end:
        days.append(current)
        current += timedelta(days=1)
    return days


def is_scheduled_day(schedule_type: str, scheduled_days: list[int], target_date: date) -> bool:
    if schedule_type == 'everyday':
        return True
    return target_date.isoweekday() in scheduled_days


def scheduled_days_between(schedule_type: str, scheduled_days: list[int], start: date, end: date) -> list[date]:
    result: list[date] = []
    for current in date_range(start, end):
        if is_scheduled_day(schedule_type, scheduled_days, current):
            result.append(current)
    return result


def format_day_list(scheduled_days: list[int]) -> str:
    if not scheduled_days:
        return '-'
    return ', '.join(ISO_TO_DAY_NAME[d] for d in scheduled_days)
