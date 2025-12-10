import unittest
import sqlite3
import os
import app  # Import your app.py

class TestAnonymization(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Use the same database as app.py
        cls.db_path = os.getenv('DATABASE_PATH', 'test_users.db')

        # Ensure folder exists if using a subfolder
        os.makedirs(os.path.dirname(cls.db_path), exist_ok=True)

        # Initialize and anonymize the database before tests
        app.init_database()
        app.anonymize_data()

    def setUp(self):
        # Connect to the database for each test
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    def tearDown(self):
        self.conn.close()

    def test_users_anonymized(self):
        self.cursor.execute("SELECT id, name, email FROM users")
        rows = self.cursor.fetchall()
        
        for user_id, name, email in rows:
            expected_email = f"anonym_{user_id}@example.com"
            self.assertEqual(name, "Anonym Användare", f"Name not anonymized for user {user_id}")
            self.assertEqual(email, expected_email, f"Email not anonymized correctly for user {user_id}")

if __name__ == "__main__":
    unittest.main()
