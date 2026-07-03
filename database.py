"""
Gerenciamento de banco de dados do A.R.G.U.S.
"""

import sqlite3
import os
from datetime import datetime
from config import DB_PATH


class DatabaseManager:
    def __init__(self):
        self.db_path = DB_PATH
        self.init_database()

    def init_database(self):
        """Inicializa o banco de dados com as tabelas necessárias"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Tabela de logs do sistema
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS system_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    cpu_usage REAL,
                    ram_usage REAL,
                    gpu_usage REAL,
                    disk_usage REAL,
                    temperature REAL,
                    internet_speed_down REAL,
                    internet_speed_up REAL,
                    processes_count INTEGER
                )
            ''')
            
            # Tabela de alertas
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS alerts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    alert_type TEXT,
                    message TEXT,
                    severity TEXT
                )
            ''')
            
            # Tabela de eventos de arquivo
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS file_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    event_type TEXT,
                    file_path TEXT
                )
            ''')
            
            # Tabela de IP e localização
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS network_info (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    public_ip TEXT,
                    city TEXT,
                    country TEXT,
                    latitude REAL,
                    longitude REAL
                )
            ''')
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Erro ao inicializar banco de dados: {e}")

    def log_system_stats(self, cpu, ram, gpu, disk, temp, down, up, processes):
        """Log das estatísticas do sistema"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO system_logs 
                (timestamp, cpu_usage, ram_usage, gpu_usage, disk_usage, temperature, internet_speed_down, internet_speed_up, processes_count)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (datetime.now().isoformat(), cpu, ram, gpu, disk, temp, down, up, processes))
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Erro ao log de stats: {e}")

    def log_alert(self, alert_type, message, severity="NORMAL"):
        """Log de alertas"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO alerts (timestamp, alert_type, message, severity)
                VALUES (?, ?, ?, ?)
            ''', (datetime.now().isoformat(), alert_type, message, severity))
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Erro ao log de alerta: {e}")

    def log_file_event(self, event_type, file_path):
        """Log de eventos de arquivo"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO file_events (timestamp, event_type, file_path)
                VALUES (?, ?, ?)
            ''', (datetime.now().isoformat(), event_type, file_path))
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Erro ao log de arquivo: {e}")

    def get_latest_stats(self, limit=100):
        """Recupera as estatísticas mais recentes"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM system_logs ORDER BY timestamp DESC LIMIT ?
            ''', (limit,))
            
            data = cursor.fetchall()
            conn.close()
            return data
        except Exception as e:
            print(f"Erro ao recuperar stats: {e}")
            return []

    def get_recent_alerts(self, limit=50):
        """Recupera os alertas recentes"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM alerts ORDER BY timestamp DESC LIMIT ?
            ''', (limit,))
            
            data = cursor.fetchall()
            conn.close()
            return data
        except Exception as e:
            print(f"Erro ao recuperar alertas: {e}")
            return []


# Instância global
db = DatabaseManager()
