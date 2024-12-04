import sqlite3

db_name = "music_quiz.db"
conn = sqlite3.connect(db_name)
cursor = conn.cursor()

def setup_database():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    )
    """)
    conn.commit()
    print("Users table is set up.")

def add_user(username, password):
    """Add a new user to the database."""
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        print(f"User {username} added successfully.")
    except sqlite3.Error as e:
        print(f"Error adding user: {e}")

def check_user(username, password):
    """Check if the user exists in the database."""
    try:
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        print(f"Checking user {username}: {'Found' if user else 'Not Found'}")
        return user
    except sqlite3.Error as e:
        print(f"Error checking user: {e}")
        return None
