def habit_saved(name: str) -> str:
    return f'Habit berhasil ditambahkan: {name}'


def habit_deleted(name: str) -> str:
    return f'Habit dihapus: {name}'


def habit_not_found() -> str:
    return 'Habit tidak ditemukan.'


def checkin_success(name: str) -> str:
    return f'Check-in berhasil untuk {name}.'


def undo_success(name: str) -> str:
    return f'Check-in hari ini dibatalkan untuk {name}.'


def already_checked_in(name: str) -> str:
    return f'{name} sudah check-in hari ini.'


def not_due_today(name: str) -> str:
    return f'Habit ini tidak dijadwalkan untuk hari ini: {name}'


def no_today_checkin(name: str) -> str:
    return f'Belum ada check-in hari ini untuk {name}.'


def no_habits() -> str:
    return 'Belum ada habit.'


def invalid_days() -> str:
    return 'Pilih minimal satu hari.'
