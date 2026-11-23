
import sqlite3
from pathlib import Path


class BatteryDatabase:
    """SQLite storage for simulated EV battery measurements."""

    def __init__(self, db_path):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.create_tables()

    def create_tables(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS battery_measurements (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    time_s REAL NOT NULL,
                    voltage_V REAL NOT NULL,
                    current_A REAL NOT NULL,
                    soc_pct REAL NOT NULL,
                    temperature_C REAL NOT NULL,
                    soh_pct REAL NOT NULL
                )
            """)

    def insert_measurement(
        self, time_s, voltage_V, current_A,
        soc_pct, temperature_C, soh_pct
    ):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO battery_measurements (
                    time_s, voltage_V, current_A,
                    soc_pct, temperature_C, soh_pct
                )
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                time_s, voltage_V, current_A,
                soc_pct, temperature_C, soh_pct
            ))

    def fetch_all(self):
        with sqlite3.connect(self.db_path) as conn:
            return conn.execute("""
                SELECT time_s, voltage_V, current_A,
                       soc_pct, temperature_C, soh_pct
                FROM battery_measurements
                ORDER BY time_s, id
            """).fetchall()
