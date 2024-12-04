import sqlite3

db_name = "user_data.db"
conn = sqlite3.connect(db_name)
cursor = conn.cursor()

def setup_user_database():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_stats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        correct_guesses INTEGER DEFAULT 0,
        incorrect_guesses INTEGER DEFAULT 0,
        skipped_questions INTEGER DEFAULT 0
    )
    """)
    conn.commit()
    print("User stats table is set up.")

def save_user_results(username, correct_guesses, incorrect_guesses, skipped_questions):
    """Save game results for a user."""
    try:
        cursor.execute("""
            INSERT INTO user_stats (username, correct_guesses, incorrect_guesses, skipped_questions)
            VALUES (?, ?, ?, ?)
        """, (username, correct_guesses, incorrect_guesses, skipped_questions))
        conn.commit()
        print(f"Results saved for user {username}.")
    except sqlite3.Error as e:
        print(f"Error saving results: {e}")
