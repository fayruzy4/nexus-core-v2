from __future__ import annotations

from app.modules.habit.texts.messages import invalid_days


def validate_name(value: str) -> str:
    value = value.strip()
    if len(value) < 2:
        raise ValueError('Nama habit terlalu pendek.')
    return value


def validate_emoji(value: str) -> str:
    value = value.strip()
    if not value:
        raise ValueError('Emoji tidak boleh kosong.')
    return value


def validate_category(value: str) -> str:
    value = value.strip()
    if not value:
        raise ValueError('Kategori tidak boleh kosong.')
    return value


def validate_selected_days(selected_days: list[int]) -> list[int]:
    if not selected_days:
        raise ValueError(invalid_days())
    return sorted(set(selected_days))
