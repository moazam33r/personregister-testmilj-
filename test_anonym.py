import sqlite3
import os
import app

class TestAnonymization:
    @classmethod
    def setup_class(cls):
        cls.db_path = os.getenv('DATABASE_PATH', 'test_users.db')
        dir_path = os.path.dirname(cls.db_path)
        if dir_path:
            os.makedirs(dir_path, exist_ok=True)
        app.init_database()
        app.anonymize_data()

    def setup_method(self):
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    def teardown_method(self):
        self.conn.close()

    def test_users_anonymized(self):
        self.cursor.execute("SELECT id, name, email FROM users")
        rows = self.cursor.fetchall()
        for user_id, name, email in rows:
            expected_email = f"anonym_{user_id}@example.com"
            assert name == "Anonym Användare", f"Name not anonymized for user {user_id}"
            assert email == expected_email, f"Email not anonymized correctly for user {user_id}"
