import sqlite3

# Create a database if nonexistent
def init_db():
    conn = sqlite3.connect("burnout.db")

    cursor = conn.cursor()

# Create users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        email TEXT UNIQUE,
        password_hash TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )

    """)
# Create daily_inputs table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS daily_inputs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        email TEXT UNIQUE,
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