"""Monitoramento do sistema."""

import os
from datetime import datetime
from typing import Optional

import psutil
from config import CPU_ALERT_THRESHOLD, RAM_ALERT_THRESHOLD, TEMP_ALERT_THRESHOLD


class SystemMonitor:
    def __init__(self):
        self.cpu_usage = self.ram_usage = self.gpu_usage = self.disk_usage = self.temperature = 0
        self.processes_count = 0
        self.suspicious_processes = []
        self.gpu_available = False

    def get_cpu_usage(self):
        self.cpu_usage = psutil.cpu_percent(interval=0.1)
        return self.cpu_usage

    def get_ram_usage(self):
        self.ram_usage = psutil.virtual_memory().percent
        return self.ram_usage

    def get_disk_usage(self):
        root = f"{os.environ.get('SystemDrive', 'C:')}\\" if os.name == "nt" else "/"
        self.disk_usage = psutil.disk_usage(root).percent
        return self.disk_usage

    def get_gpu_usage(self):
        """Obtém GPU NVIDIA quando NVML está disponível; nunca simula uma métrica."""
        try:
            import pynvml
            pynvml.nvmlInit()
            handle = pynvml.nvmlDeviceGetHandleByIndex(0)
            self.gpu_usage = pynvml.nvmlDeviceGetUtilizationRates(handle).gpu
            self.gpu_available = True
        except (ImportError, Exception):
            self.gpu_usage = 0
            self.gpu_available = False
        return self.gpu_usage

    def get_temperature(self):
        try:
            temps = psutil.sensors_temperatures()
            for readings in temps.values():
                if readings:
                    self.temperature = readings[0].current
                    return self.temperature
        except (AttributeError, OSError):
            pass
        self.temperature = 0
        return 0

    def get_processes_count(self):
        self.processes_count = len(psutil.pids())
        return self.processes_count

    def get_suspicious_processes(self):
        """Retorna processos de alto consumo; isto não é uma classificação de malware."""
        candidates = []
        for proc in psutil.process_iter(["pid", "name", "cpu_percent", "memory_percent"]):
            try:
                cpu, memory = proc.info["cpu_percent"] or 0, proc.info["memory_percent"] or 0
                if cpu > 50 or memory > 20:
                    candidates.append({"name": proc.info["name"], "pid": proc.info["pid"], "cpu": cpu, "memory": memory})
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        self.suspicious_processes = sorted(candidates, key=lambda item: max(item["cpu"], item["memory"]), reverse=True)[:10]
        return self.suspicious_processes

    def get_network_connections(self):
        counters = psutil.net_io_counters()
        return {key: getattr(counters, key) for key in ("bytes_sent", "bytes_recv", "packets_sent", "packets_recv", "errin", "errout")}

    def get_boot_time(self):
        return datetime.fromtimestamp(psutil.boot_time()).isoformat(timespec="seconds")

    def get_all_stats(self):
        return {"cpu": self.get_cpu_usage(), "ram": self.get_ram_usage(), "gpu": self.get_gpu_usage(),
                "gpu_available": self.gpu_available, "disk": self.get_disk_usage(), "temperature": self.get_temperature(),
                "processes": self.get_processes_count(), "boot_time": self.get_boot_time(),
                "network": self.get_network_connections(), "high_usage_processes": self.get_suspicious_processes()}

    def check_alerts(self, stats: Optional[dict] = None):
        values = stats or self.get_all_stats()
        limits = (("TEMPERATURA_ALTA", "temperature", TEMP_ALERT_THRESHOLD, "Temperatura crítica"),
                  ("CPU_ALTA", "cpu", CPU_ALERT_THRESHOLD, "Uso de CPU crítico"),
                  ("RAM_ALTA", "ram", RAM_ALERT_THRESHOLD, "Uso de RAM crítico"))
        return [(kind, f"{label}: {values[key]:.1f}") for kind, key, threshold, label in limits if values[key] > threshold]


monitor = SystemMonitor()

