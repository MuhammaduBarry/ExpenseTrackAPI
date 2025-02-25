import sqlite3

def create_user_table():
    conn = sqlite3.connect("users.db")
    conn.row_factory = sqlite3.Row # Allow for both rows and dict access

    try:
        cursor = conn.cursor()
        # Create Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT NOT NULL,
                password TEXT not NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.commit()
    except Exception as e:
        print(e)
    finally:
        conn.close()

def connect_db():
    conn = sqlite3.connect("users.db")
    conn.row_factory = sqlite3.Row  # Allow for both rows and dict access

    return conn