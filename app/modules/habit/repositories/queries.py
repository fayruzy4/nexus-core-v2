GET_HABIT_BY_ID = """
SELECT *
FROM habits
WHERE id = $1 AND owner_telegram_id = $2
"""

LIST_HABITS_BY_OWNER = """
SELECT *
FROM habits
WHERE owner_telegram_id = $1
ORDER BY id ASC
"""

CREATE_HABIT = """
INSERT INTO habits (
    owner_telegram_id,
    name,
    emoji,
    category,
    schedule_type,
    scheduled_days
)
VALUES ($1, $2, $3, $4, $5, $6)
RETURNING *
"""

DELETE_HABIT = """
DELETE FROM habits
WHERE id = $1 AND owner_telegram_id = $2
RETURNING id, name
"""

INSERT_CHECKIN = """
INSERT INTO habit_checkins (habit_id, checkin_date)
VALUES ($1, $2)
RETURNING id
"""

DELETE_CHECKIN = """
DELETE FROM habit_checkins
WHERE habit_id = $1 AND checkin_date = $2
RETURNING id
"""

GET_CHECKIN_BY_DATE = """
SELECT id
FROM habit_checkins
WHERE habit_id = $1 AND checkin_date = $2
"""

LIST_CHECKINS_BY_HABIT = """
SELECT checkin_date
FROM habit_checkins
WHERE habit_id = $1
ORDER BY checkin_date ASC
"""

LIST_CHECKINS_BY_OWNER_RANGE = """
SELECT hc.checkin_date, h.id AS habit_id, h.schedule_type, h.scheduled_days, h.created_at
FROM habit_checkins hc
JOIN habits h ON h.id = hc.habit_id
WHERE h.owner_telegram_id = $1
  AND hc.checkin_date BETWEEN $2 AND $3
ORDER BY hc.checkin_date ASC, h.id ASC
"""

LIST_HABITS_WITH_IDS_BY_OWNER = """
SELECT id, name, emoji, category, schedule_type, scheduled_days, current_streak, longest_streak, total_completion, total_missed, created_at
FROM habits
WHERE owner_telegram_id = $1
ORDER BY id ASC
"""

UPDATE_HABIT_STATS = """
UPDATE habits
SET current_streak = $1,
    longest_streak = $2,
    total_completion = $3,
    total_missed = $4
WHERE id = $5 AND owner_telegram_id = $6
RETURNING *
"""
