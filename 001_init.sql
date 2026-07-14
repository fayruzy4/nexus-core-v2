CREATE TABLE IF NOT EXISTS habits (
    id BIGSERIAL PRIMARY KEY,
    owner_telegram_id BIGINT NOT NULL,
    name TEXT NOT NULL,
    emoji TEXT NOT NULL,
    category TEXT NOT NULL,
    schedule_type TEXT NOT NULL CHECK (schedule_type IN ('everyday', 'custom')),
    scheduled_days SMALLINT[] NOT NULL DEFAULT '{}',
    current_streak INTEGER NOT NULL DEFAULT 0,
    longest_streak INTEGER NOT NULL DEFAULT 0,
    total_completion INTEGER NOT NULL DEFAULT 0,
    total_missed INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_habits_owner_telegram_id ON habits (owner_telegram_id);

CREATE TABLE IF NOT EXISTS habit_checkins (
    id BIGSERIAL PRIMARY KEY,
    habit_id BIGINT NOT NULL REFERENCES habits(id) ON DELETE CASCADE,
    checkin_date DATE NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (habit_id, checkin_date)
);

CREATE INDEX IF NOT EXISTS idx_habit_checkins_habit_id ON habit_checkins (habit_id);
CREATE INDEX IF NOT EXISTS idx_habit_checkins_checkin_date ON habit_checkins (checkin_date);
