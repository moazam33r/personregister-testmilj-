import sqlite3
import os
import logging

# -----------------------------
# Grundläggande konfiguration
# -----------------------------

logging.basicConfig(level=logging.INFO)


# -----------------------------
# Hjälpfunktioner
# -----------------------------

def get_db_path():
    """
    Returnerar en säker sökväg till databasen i samma mapp som app.py.
    Detta löser problemet med att /data/ inte finns på macOS.
    """
    base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, "test_users.db")


def open_conn():
    """
    Öppnar en databasanslutning mot SQLite-databasen.
    """
    return sqlite3.connect(get_db_path())


# -----------------------------
# Databasfunktioner
# -----------------------------

def init_db():
    """
    Skapar tabellen 'users' om den inte finns och fyller testdata
    om databasen är tom.
    """
    with open_conn() as conn:
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE
            )
        """)

        cur.execute("SELECT COUNT(*) FROM users")
        already_exists = cur.fetchone()[0]

        if already_exists == 0:
            initial_users = [
                ("Karin Karlsson", "karin@example.test"),
                ("Erik Eriksson", "erik@example.test")
            ]

            cur.executemany(
                "INSERT INTO users (name, email) VALUES (?, ?)",
                initial_users
            )

            logging.info("Databasen initierades med testanvändare.")
        else:
            logging.info("Databasen innehåller redan data.")


def get_all_users():
    """
    Hämtar alla användare som en lista av dictionaries.
    """
    with open_conn() as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, name, email FROM users")
        rows = cur.fetchall()
        return [{"id": r[0], "name": r[1], "email": r[2]} for r in rows]


def display_users():
    """
    Skriver ut alla användare i konsolen.
    """
    users = get_all_users()

    if not users:
        logging.info("Inga användare hittades.")
        return

    logging.info("Nuvarande användare:")
    for user in users:
        logging.info(f"- ID: {user['id']} | Namn: {user['name']} | Email: {user['email']}")


def anonymize_users():
    """
    Anonymiserar alla användare.
    """
    with open_conn() as conn:
        cur = conn.cursor()

        cur.execute("""
            UPDATE users
            SET
                name = 'Anonym Användare',
                email = 'anonymiserad@example.test'
        """)

        conn.commit()
        affected = cur.rowcount

    logging.info(f"{affected} användare anonymiserades.")
    return affected


def clear_users():
    """
    Tar bort alla användare.
    """
    with open_conn() as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM users")
        conn.commit()
        removed = cur.rowcount

    logging.info(f"{removed} användare raderades.")
    return removed


# -----------------------------
# Kör applikationen
# -----------------------------

if __name__ == "__main__":
    logging.info("Startar applikationen...")
    init_db()
    display_users()
