import sqlite3
import threading

class CogniQDatabase:
    _lock = threading.Lock()

    def __init__(self, db_path='cogniq_database.db'):
        self.db_path = db_path
        
    def _connect(self):
        return sqlite3.connect(self.db_path)

    def get_all_users(self):
        with self._lock:
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute("SELECT email FROM users")
            users = [row[0] for row in cursor.fetchall()]
            conn.close()
            return users

    def get_journals(self, user_email):
        with self._lock:
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT content, date FROM journal_entries WHERE email = ? ORDER BY date ASC",
                (user_email,)
            )
            results = cursor.fetchall()
            conn.close()
            return results

    def get_moods(self, user_email):
        with self._lock:
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT mood_level, date FROM mood_entries WHERE email = ? ORDER BY date ASC",
                (user_email,)
            )
            results = cursor.fetchall()
            conn.close()
            moods = [{'mood_level': row[0], 'date': row[1]} for row in results]
            return moods

    def save_journal(self, user_email, content):
        with self._lock:
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO journal_entries (email, content, date) VALUES (?, ?, datetime('now'))",
                (user_email, content)
            )
            conn.commit()
            conn.close()

    def save_mood(self, user_email, mood_level):
        with self._lock:
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO mood_entries (email, mood_level, date) VALUES (?, ?, datetime('now'))",
                (user_email, mood_level)
            )
            conn.commit()
            conn.close()
