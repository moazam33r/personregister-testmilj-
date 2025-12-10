import sqlite3
import os

# Use environment variable DATABASE_PATH or default to relative path 'test_users.db'
db_path = os.getenv('DATABASE_PATH', 'test_users.db')

# Only create folder if db_path has a directory
dir_path = os.path.dirname(db_path)
if dir_path:
    os.makedirs(dir_path, exist_ok=True)

def init_database():
    """Initialize the database and create users table"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL
        )
    ''')
    
    cursor.execute('SELECT COUNT(*) FROM users')
    count = cursor.fetchone()[0]
    
    if count == 0:
        test_users = [
            ('Anna Andersson', 'anna@test.se'),
            ('Bo Bengtsson', 'bo@test.se')
        ]
        cursor.executemany('INSERT INTO users (name, email) VALUES (?, ?)', test_users)
        print("Database initialized with test users")
    else:
        print(f"Database already contains {count} users")
    
    conn.commit()
    conn.close()

def display_users():
    """Display all users in the database"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    
    print("\nCurrent users in database:")
    for user in users:
        print(f"ID: {user[0]}, Name: {user[1]}, Email: {user[2]}")
    
    conn.close()

def clear_test_data():
    """GDPR Action 1: Clear all test data"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM users')
    conn.commit()
    conn.close()
    print("All test data has been cleared (GDPR compliant)")

def anonymize_data():
    """GDPR Action 2: Anonymize user data (names + emails)"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('SELECT id FROM users')
    users = cursor.fetchall()

    for user in users:
        user_id = user[0]
        anonym_email = f"anonym_{user_id}@example.com"
        cursor.execute('''
            UPDATE users
            SET name = "Anonym Användare",
                email = ?
            WHERE id = ?
        ''', (anonym_email, user_id))

    conn.commit()
    conn.close()
    print("All user names and emails have been anonymized (GDPR compliant)")

if __name__ == "__main__":
    init_database()
    display_users()
    
    print("\nContainer is running. Press Ctrl+C to exit.")
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("\nShutting down...")
