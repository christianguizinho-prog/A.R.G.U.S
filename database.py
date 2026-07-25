"""Persistência SQLite do A.R.G.U.S."""

import sqlite3
from datetime import datetime
from pathlib import Path

from config import DB_PATH, MAX_HISTORY


class DatabaseManager:
    def __init__(self):
        self.db_path = DB_PATH
        self.init_database()

    def _connect(self):
        connection = sqlite3.connect(self.db_path, timeout=5)
        connection.row_factory = sqlite3.Row
        return connection

    def init_database(self):
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as conn:
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS system_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT NOT NULL,
                    cpu_usage REAL, ram_usage REAL, gpu_usage REAL, disk_usage REAL,
                    temperature REAL, internet_speed_down REAL, internet_speed_up REAL, processes_count INTEGER
                );
                CREATE TABLE IF NOT EXISTS alerts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT NOT NULL,
                    alert_type TEXT NOT NULL, message TEXT NOT NULL, severity TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS file_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT NOT NULL, event_type TEXT NOT NULL, file_path TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS network_info (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT NOT NULL, public_ip TEXT, city TEXT, country TEXT, latitude REAL, longitude REAL
                );
                CREATE INDEX IF NOT EXISTS idx_system_logs_timestamp ON system_logs(timestamp DESC);
                CREATE INDEX IF NOT EXISTS idx_alerts_timestamp ON alerts(timestamp DESC);
            """)

    def log_system_stats(self, cpu, ram, gpu, disk, temp, down, up, processes):
        with self._connect() as conn:
            conn.execute("""INSERT INTO system_logs (timestamp,cpu_usage,ram_usage,gpu_usage,disk_usage,temperature,internet_speed_down,internet_speed_up,processes_count)
                         VALUES (?,?,?,?,?,?,?,?,?)""", (datetime.now().isoformat(), cpu, ram, gpu, disk, temp, down, up, processes))
            conn.execute("DELETE FROM system_logs WHERE id NOT IN (SELECT id FROM system_logs ORDER BY id DESC LIMIT ?)", (MAX_HISTORY,))

    def log_alert(self, alert_type, message, severity="NORMAL"):
        with self._connect() as conn:
            conn.execute("INSERT INTO alerts (timestamp,alert_type,message,severity) VALUES (?,?,?,?)", (datetime.now().isoformat(), alert_type, message, severity))

    def log_file_event(self, event_type, file_path):
        with self._connect() as conn:
            conn.execute("INSERT INTO file_events (timestamp,event_type,file_path) VALUES (?,?,?)", (datetime.now().isoformat(), event_type, file_path))

    def get_latest_stats(self, limit=100):
        limit = min(max(int(limit), 1), 1_000)
        with self._connect() as conn:
            return [dict(row) for row in conn.execute("SELECT * FROM system_logs ORDER BY timestamp DESC LIMIT ?", (limit,))]

    def get_recent_alerts(self, limit=50):
        limit = min(max(int(limit), 1), 1_000)
        with self._connect() as conn:
            return [dict(row) for row in conn.execute("SELECT * FROM alerts ORDER BY timestamp DESC LIMIT ?", (limit,))]


db = DatabaseManager()
