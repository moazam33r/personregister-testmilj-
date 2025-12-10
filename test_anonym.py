import unittest
import sqlite3
import os

class TestAnonymization(unittest.TestCase):
    def setUp(self):
        # Använd samma databas som i workflow
        self.db_path = os.getenv('DATABASE_PATH', '/data/test_users.db')
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
