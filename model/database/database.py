import sqlite3
from werkzeug.security import generate_password_hash

# Add a new user to the database
def add_user(email, password):
    conn = sqlite3.connect("burnout.db")
    cursor = conn.cursor()
    # Hash the password for security
    hashed_pwd = generate_password_hash(password)
    
    try:
        # Insert the new user into the users table
        cursor.execute(
            "INSERT INTO users (email, password_hash) VALUES (?, ?)",
            (email, hashed_pwd)
        )
        conn.commit()
        user_id = cursor.lastrowid  # get the ID of the newly created user
        
    # prevents duplicate emails
    except sqlite3.IntegrityError:
        user_id = None
        
    conn.close()
    return user_id

# Retrieve a user by email
def user_by_email(email):
    conn = sqlite3.connect("burnout.db")
    conn.row_factory = sqlite3.Row  # allows dict-like access to columns
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT * FROM users WHERE email = ?",
        (email,)
    )
    
    # returning a single row as a sqlite3.Row object
    user = cursor.fetchone()
    conn.close()
    
    # convert sqlite3.Row to a regular dict so it can be used easily
    # and avoid binding errors when passing to other functions
    return dict(user) if user else None

# Add daily input data for a user
def add_daily_input(
    user_id,
    sleep_hours,
    mood,
    physical_activity,
    cups_water,
    cups_caffeine,
    last_meal,
    score,
    created_at
):
    conn = sqlite3.connect("burnout.db")
    cursor = conn.cursor()
    
    # insert daily tracking data into the database
    cursor.execute("""
        INSERT INTO daily_inputs
        (user_id, sleep_hours, mood, physical_activity,
        cups_water, cups_caffeine, last_meal, score, created_at) VALUES
        (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        sleep_hours,
        mood,
        physical_activity,
        cups_water,
        cups_caffeine,
        last_meal,
        score,
        created_at
    ))
    
    conn.commit()
    conn.close()

# Find the number of meals logged by a user today
def find_meals(user_id):
    # connect to the sqlite database
    conn = sqlite3.connect("burnout.db")
    cursor = conn.cursor()
    
    # count today's meals by checking if last_meal date matches today's date
    cursor.execute("""
        SELECT COUNT(*) as today_count
        FROM daily_inputs
        WHERE user_id = ? AND DATE(last_meal) = DATE('now')     
    """, (user_id,))
    
    # fetch the result from the query
    result = cursor.fetchone()
    conn.close()
    
    # result is a tuple, so access the first element (index 0)
    # if no result exists, default to 0
    return int(result[0]) if result else 0