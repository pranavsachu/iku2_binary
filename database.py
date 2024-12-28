import sqlite3

def initialize_db():
    conn = sqlite3.connect("iku.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            credits REAL DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

def register_user(username, password):
    try:
        conn = sqlite3.connect("iku.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

def validate_user(username, password):
    conn = sqlite3.connect("iku.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user

def get_user_credits(user_id):
    conn = sqlite3.connect("iku.db")
    cursor = conn.cursor()
    cursor.execute("SELECT credits FROM users WHERE id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else 0

def update_user_credits(user_id, amount):
    conn = sqlite3.connect("iku.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET credits = credits + ? WHERE id = ?", (amount, user_id))
    conn.commit()
    conn.close()
