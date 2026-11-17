import sqlite3

SCHEMA = """
CREATE TABLE IF NOT EXISTS tutors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    subjects TEXT NOT NULL DEFAULT '',
    photo INTEGER NOT NULL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tutor_id INTEGER NOT NULL REFERENCES tutors(id),
    student_id INTEGER NOT NULL REFERENCES students(id),
    start TEXT NOT NULL,
    "end" TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'active',
    created_at TEXT NOT NULL,
    cancelled_at TEXT
);
CREATE INDEX IF NOT EXISTS idx_bookings_tutor ON bookings(tutor_id, start);
CREATE INDEX IF NOT EXISTS idx_bookings_student ON bookings(student_id, start);
"""


def connect(path: str = ":memory:") -> sqlite3.Connection:
    conn = sqlite3.connect(path, check_same_thread=False, isolation_level=None)
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA)
    # migración: bases creadas antes de RF1 (foto) no tienen la columna
    cols = [r["name"] for r in conn.execute("PRAGMA table_info(tutors)")]
    if "photo" not in cols:
        conn.execute("ALTER TABLE tutors ADD COLUMN photo INTEGER NOT NULL DEFAULT 0")
    return conn
