import sqlite3
import os
import app

class TestAnonymization:
    # körs en gång innan alla tester för att initiera databasen och anonymisera data
    @classmethod
    def setup_class(cls):
        # hämtar databasens sökväg från miljövariabel eller använder standardvärde
        cls.db_path = os.getenv('DATABASE_PATH', 'test_users.db')
        # skapar katalogen om den inte finns
        dir_path = os.path.dirname(cls.db_path)
        if dir_path:
            os.makedirs(dir_path, exist_ok=True)
        # initierar databasen och anonymiserar data
        app.init_database()
        app.anonymize_data()
    # körs före varje testmetod 
    def setup_method(self):
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    def teardown_method(self):
        self.conn.close()
    
    def test_users_anonymized(self):
        self.cursor.execute("SELECT id, name, email FROM users")
        rows = self.cursor.fetchall()
        # verifierar att alla användare är anonymiserade
        for user_id, name, email in rows:
            expected_email = f"anonym_{user_id}@example.com"
            # Kontrollera att namn och email är anonymiserade
            assert name == "Anonym Användare", f"Name not anonymized for user {user_id}"
            assert email == expected_email, f"Email not anonymized correctly for user {user_id}"
