from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    project_name: str
    bot_name: str
    bot_token: str
    owner_telegram_id: int
    database_dsn: str
    log_level: str
    tz: str



def load_settings() -> Settings:
    bot_token = os.getenv('BOT_TOKEN', '').strip()
    owner_raw = os.getenv('OWNER_TELEGRAM_ID', '').strip()
    database_dsn = os.getenv('DATABASE_DSN', '').strip()

    if not bot_token:
        raise RuntimeError('BOT_TOKEN tidak boleh kosong.')
    if not owner_raw:
        raise RuntimeError('OWNER_TELEGRAM_ID tidak boleh kosong.')
    if not database_dsn:
        raise RuntimeError('DATABASE_DSN tidak boleh kosong.')

    return Settings(
        project_name=os.getenv('PROJECT_NAME', 'NEXUS CORE V2').strip(),
        bot_name=os.getenv('BOT_NAME', 'NEXUS CORE V2').strip(),
        bot_token=bot_token,
        owner_telegram_id=int(owner_raw),
        database_dsn=database_dsn,
        log_level=os.getenv('LOG_LEVEL', 'INFO').strip(),
        tz=os.getenv('TZ', 'Asia/Jakarta').strip(),
    )
