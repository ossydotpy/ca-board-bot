# db_handler.py
import sqlite3
from datetime import datetime


class DatabaseHandler:
    def __init__(self, db_path="clipboard.db"):
        self.conn = sqlite3.connect(db_path)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS contracts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                contract_address TEXT NOT NULL,
                server_id INTEGER NOT NULL,
                discord_user_id INTEGER NOT NULL,
                call BOOLEAN NOT NULL DEFAULT 0 CHECK (call IN (0, 1)),
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """
        )
        cursor.execute(
            "CREATE UNIQUE INDEX IF NOT EXISTS unique_contract_per_server ON contracts (contract_address, server_id)"
        )
        self.conn.commit()

    def add_contract(self, contract_address, server_id, discord_user_id, call):
        cursor = self.conn.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO contracts 
                (contract_address, server_id, discord_user_id, call) 
                VALUES (?, ?, ?,?)
            """,
                (contract_address, server_id, discord_user_id, call),
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            # Ignore duplicates
            return False

    def get_recent_contracts(self, server_id, limit=10):
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT contract_address, discord_user_id, timestamp 
            FROM contracts 
            WHERE server_id = ? 
            ORDER BY timestamp DESC 
            LIMIT ?
        """,
            (server_id, limit),
        )
        return cursor.fetchall()

    def close(self):
        self.conn.close()
