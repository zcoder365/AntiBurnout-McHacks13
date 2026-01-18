import sqlite3

def init_db():
#create a database if nonexistent
    conn = sqlite3.connect("burnout.db")

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        email TEXT_UNIQUE,
        password_hash TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )

    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS daily_inputs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER
        email TEXT_UNIQUE,
        sleep_hours TEXT,
        mood TEXT,
        physical_activity TEXT,
        cups_water FLOAT,
        cups_caffeine FLOAT,
        last_meal TIMESTAMP,
        score FLOAT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )

    """)

    conn.commit()
    conn.close()