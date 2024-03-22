import sqlite3


class DBManager:
    def __init__(self, db_file: str) -> None:
        self.db_file = db_file
        self.conn = sqlite3.connect(self.db_file)
        self.conn.execute(
            "CREATE TABLE IF NOT EXISTS data (id INTEGER PRIMARY KEY AUTOINCREMENT, filename TEXT NOT NULL, content BLOB NOT NULL, filetype TEXT NOT NULL, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)"
        )
        self.conn.commit()

    def get_handler(self):
        return self.conn

    def insert_file(self, filename: str, content: bytes, filetype: str) -> None:
        self.conn.execute(
            "INSERT INTO data (filename, content, filetype) VALUES (?, ?, ?)",
            (filename, content, filetype),
        )
        self.conn.commit()

    def get_file(self, filename: str) -> tuple:
        cursor = self.conn.execute("SELECT * FROM data WHERE filename = ?", (filename,))
        return cursor.fetchone()

    def delete_file(self, filename: str) -> None:
        self.conn.execute("DELETE FROM data WHERE filename = ?", (filename,))
        self.conn.commit()
