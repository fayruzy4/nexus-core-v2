# NEXUS CORE V2

Bot pribadi Telegram berbasis Python + aiogram + asyncpg + PostgreSQL.
Fokus awal: modul Habit.

## Nama sinkron yang dipakai

- Project / repo: `nexus-core-v2`
- Python package: `nexus_core_v2`
- Bot display name: `NEXUS CORE V2`
- Database: `nexus_core_v2`

## Stack

- Python 3.10+
- aiogram 3 (async Telegram framework)
- asyncpg
- PostgreSQL
- ReplyKeyboardMarkup
- python-dotenv
- matplotlib untuk chart evaluasi

## Instalasi

### 1) Buat virtual environment

```bash
python -m venv .venv
```

Aktivasi:

```bash
# Linux / macOS
source .venv/bin/activate

# Windows PowerShell
.venv\Scripts\Activate.ps1

# Windows CMD
.venv\Scriptsctivate.bat
```

Dokumentasi resmi Python menjelaskan `venv` sebagai alat standar untuk membuat virtual environment. citeturn373174search2turn373174search6

### 2) Install dependency

```bash
pip install -r requirements.txt
```

### 3) Siapkan file `.env`

Salin `.env.example` menjadi `.env`, lalu isi nilainya.

`python-dotenv` membaca pasangan key-value dari file `.env` dan memasukkannya ke environment process. citeturn853877search0

### 4) Buat database PostgreSQL

Jalankan SQL schema:

```bash
psql -U postgres -d nexus_core_v2 -f sql/001_init.sql
```

PostgreSQL memakai `CREATE TABLE` untuk membuat tabel kosong baru. citeturn373174search3turn373174search18

### 5) Jalankan bot

```bash
python -m app.main
```

Aiogram adalah framework Telegram Bot API yang asinkron, dan long-polling dijalankan lewat `Dispatcher.start_polling()` atau `Dispatcher.run_polling()`. citeturn622264search6turn622264search0turn622264search2

## Environment variables

Wajib:

- `BOT_TOKEN` → token dari BotFather
- `OWNER_TELEGRAM_ID` → Telegram ID owner
- `DATABASE_DSN` → DSN PostgreSQL

Opsional:

- `PROJECT_NAME`
- `BOT_NAME`
- `LOG_LEVEL`
- `TZ`

## Catatan implementasi

- Bot ini private, satu owner.
- Semua modul dipecah kecil.
- Reply keyboard dipakai untuk navigasi.
- SQL native dipakai lewat asyncpg prepared statements.
- Tidak ada ORM.
