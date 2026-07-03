"""
Monitoramento do sistema - A.R.G.U.S.
"""

import psutil
import os
from datetime import datetime
from config import TEMP_ALERT_THRESHOLD, CPU_ALERT_THRESHOLD, RAM_ALERT_THRESHOLD


class SystemMonitor:
    def __init__(self):
        self.cpu_usage = 0
        self.ram_usage = 0
        self.gpu_usage = 0
        self.disk_usage = 0
        self.temperature = 0
        self.processes_count = 0
        self.suspicious_processes = []

    def get_cpu_usage(self):
        """Obtém o uso da CPU em porcentagem"""
        try:
            self.cpu_usage = psutil.cpu_percent(interval=0.1)
            return self.cpu_usage
        except Exception as e:
            print(f"Erro ao obter CPU: {e}")
            return 0

    def get_ram_usage(self):
        """Obtém o uso de RAM em porcentagem"""
        try:
            self.ram_usage = psutil.virtual_memory().percent
            return self.ram_usage
        except Exception as e:
            print(f"Erro ao obter RAM: {e}")
            return 0

    def get_disk_usage(self):
        """Obtém o uso de disco em porcentagem"""
        try:
            self.disk_usage = psutil.disk_usage('/').percent
            return self.disk_usage
        except Exception as e:
            print(f"Erro ao obter disco: {e}")
            return 0

    def get_gpu_usage(self):
        """
        Obtém o uso de GPU (simulado, pois depende do driver NVIDIA)
        Para sistema real, seria necessário nvidia-ml-py
        """
        try:
            # Simulação para demonstração
            self.gpu_usage = psutil.cpu_percent() * 0.6
            return min(self.gpu_usage, 100)
        except Exception as e:
            print(f"Erro ao obter GPU: {e}")
            return 0

    def get_temperature(self):
        """Obtém a temperatura da CPU"""
        try:
            if not hasattr(psutil, 'sensors_temperatures'):
                return 0

            temps = psutil.sensors_temperatures()
            if not temps:
                return 0

            if 'coretemp' in temps:
                self.temperature = temps['coretemp'][0].current
            elif 'acpitz' in temps:
                self.temperature = temps['acpitz'][0].current
            else:
                # Usar uma lista das temperaturas disponíveis
                for temp_list in temps.values():
                    if temp_list:
                        self.temperature = temp_list[0].current
                        break
            return self.temperature
        except Exception as e:
            print(f"Erro ao obter temperatura: {e}")
            return 0

    def get_processes_count(self):
        """Obtém a contagem de processos em execução"""
        try:
            self.processes_count = len(psutil.pids())
            return self.processes_count
        except Exception as e:
            print(f"Erro ao obter processos: {e}")
            return 0

    def get_suspicious_processes(self):
        """
        Analisa e retorna processos suspeitos
        (Aqui uma análise simples - pode ser expandida)
        """
        try:
            suspicious = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    if proc.info['cpu_percent'] and proc.info['cpu_percent'] > 50:
                        suspicious.append({
                            'name': proc.info['name'],
                            'pid': proc.info['pid'],
                            'cpu': proc.info['cpu_percent'],
                            'memory': proc.info['memory_percent']
                        })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            
            self.suspicious_processes = suspicious[:10]  # Top 10
            return self.suspicious_processes
        except Exception as e:
            print(f"Erro ao analisar processos suspeitos: {e}")
            return []

    def get_network_connections(self):
        """Obtém estatísticas de conexões de rede"""
        try:
            net_io = psutil.net_io_counters()
            return {
                'bytes_sent': net_io.bytes_sent,
                'bytes_recv': net_io.bytes_recv,
                'packets_sent': net_io.packets_sent,
                'packets_recv': net_io.packets_recv,
                'errin': net_io.errin,
                'errout': net_io.errout
            }
        except Exception as e:
            print(f"Erro ao obter conexões de rede: {e}")
            return {}

    def get_boot_time(self):
        """Obtém o tempo de inicialização do sistema"""
        try:
            boot_time = datetime.fromtimestamp(psutil.boot_time())
            return boot_time.strftime('%Y-%m-%d %H:%M:%S')
        except Exception as e:
            print(f"Erro ao obter tempo de boot: {e}")
            return "Desconhecido"

    def get_all_stats(self):
        """Retorna todas as estatísticas do sistema"""
        return {
            'cpu': self.get_cpu_usage(),
            'ram': self.get_ram_usage(),
            'gpu': self.get_gpu_usage(),
            'disk': self.get_disk_usage(),
            'temperature': self.get_temperature(),
            'processes': self.get_processes_count(),
            'boot_time': self.get_boot_time(),
            'network': self.get_network_connections(),
            'suspicious': self.get_suspicious_processes()
        }

    def check_alerts(self):
        """Verifica se há alertas para gerar"""
        alerts = []
        
        if self.temperature > TEMP_ALERT_THRESHOLD:
            alerts.append(('TEMPERATURA_ALTA', f'Temperatura crítica: {self.temperature:.1f}°C'))
        
        if self.cpu_usage > CPU_ALERT_THRESHOLD:
            alerts.append(('CPU_ALTA', f'Uso de CPU crítico: {self.cpu_usage:.1f}%'))
        
        if self.ram_usage > RAM_ALERT_THRESHOLD:
            alerts.append(('RAM_ALTA', f'Uso de RAM crítico: {self.ram_usage:.1f}%'))
        
        return alerts


# Instância global
monitor = SystemMonitor()
