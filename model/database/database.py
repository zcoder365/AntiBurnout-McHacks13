import sqlite3
from werkzeug.security import generate_password_hash

def add_user(email, password):
    
    conn = sqlite3.connect("burnout.db")
    cursor = conn.cursor()

    #Hash the password
    hashed_pwd = generate_password_hash(password)

    try:
        #creates a new user with the email and password into a row
        cursor.execute(
            "INSERT INTO users (email, password_hash) VALUES (?, ?)",
            (email, hashed_pwd)
        )
        conn.commit()
        user_id = cursor.lastrowid
    
    except sqlite3.IntegrityError:
        user_id = None
    
    conn.close()
    return user_id

def user_by_email(email):
    conn = sqlite3.connect("burnout.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE email = ?",
        (email,)
    )
    #returning a single tuple
    user = cursor.fetchone()
    conn.close()
    return user

def add_daily_input(
    user_id,
    sleep_hours,
    mood,
    physical_activity,
    cups_water,
    cups_caffeine,
    last_meal,
    created_at
):
    conn = sqlite3.connect("burnout.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO daily_inputs
        (user_id, sleep_hours, mood, physical_activity,
        cups_water, cups_caffeine, last_meal, created_at) VALUES
        (?, ?, ?, ?, ?, ?, ?, ?)
    
    """, (
        user_id,
        sleep_hours,
        mood,
        physical_activity,
        cups_water,
        cups_caffeine,
        last_meal,
        created_at
    ))
    conn.commit()
    conn.close()


def find_meals(user_id):
    conn = sqlite3.connect("burnout.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*) as today_count
        FROM daily_inputs
        WHERE user_id = ? AND DATE(last_meal) = DATE('now')     
    """, (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result["today_count"] if result else 0



    