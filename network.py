"""
Monitoramento de rede - A.R.G.U.S.
"""

import requests
import threading
import socket
from speedtest import Speedtest
from datetime import datetime


class NetworkMonitor:
    def __init__(self):
        self.public_ip = "Buscando..."
        self.city = "---"
        self.country = "---"
        self.latitude = 0
        self.longitude = 0
        self.internet_down = 0  # Mbps
        self.internet_up = 0    # Mbps
        self.is_online = False
        self.last_speed_test = None

    def get_public_ip(self):
        """Obtém o IP público do usuário"""
        try:
            response = requests.get('https://api.ipify.org', timeout=5)
            self.public_ip = response.text.strip()
            return self.public_ip
        except Exception as e:
            print(f"Erro ao obter IP público: {e}")
            return "Offline"

    def get_location(self):
        """Obtém localização aproximada baseada no IP"""
        if not self.is_online or self.public_ip in ("Offline", "Erro", ""):
            return {
                'city': self.city,
                'country': self.country,
                'latitude': self.latitude,
                'longitude': self.longitude
            }

        try:
            response = requests.get(f'https://ipapi.co/{self.public_ip}/json/', timeout=5)
            data = response.json()
            
            self.city = data.get('city', '---')
            self.country = data.get('country_name', '---')
            self.latitude = data.get('latitude', 0)
            self.longitude = data.get('longitude', 0)
            
            return {
                'city': self.city,
                'country': self.country,
                'latitude': self.latitude,
                'longitude': self.longitude
            }
        except Exception as e:
            print(f"Erro ao obter localização: {e}")
            self.city = self.city or '---'
            self.country = self.country or '---'
            self.latitude = self.latitude or 0
            self.longitude = self.longitude or 0
            return {
                'city': self.city,
                'country': self.country,
                'latitude': self.latitude,
                'longitude': self.longitude
            }

    def check_internet(self):
        """Verifica se há conexão com a internet"""
        try:
            requests.get('https://www.google.com', timeout=2)
            self.is_online = True
            return True
        except Exception as e:
            print(f"Erro ao verificar internet: {e}")
            self.is_online = False
            return False

    def test_speed(self):
        """
        Testa a velocidade da internet
        (Este teste pode levar de 1 a 5 minutos)
        Executar em thread separada!
        """
        try:
            st = Speedtest()
            st.get_best_server()
            
            down = st.download() / 1_000_000  # Converter para Mbps
            up = st.upload() / 1_000_000      # Converter para Mbps
            
            self.internet_down = round(down, 2)
            self.internet_up = round(up, 2)
            self.last_speed_test = datetime.now()
            
            return {
                'download': self.internet_down,
                'upload': self.internet_up,
                'timestamp': self.last_speed_test
            }
        except Exception as e:
            print(f"Erro ao testar velocidade: {e}")
            return None

    def test_speed_async(self, callback=None):
        """Testa velocidade em thread separada"""
        def run_test():
            result = self.test_speed()
            if callback:
                callback(result)
        
        thread = threading.Thread(target=run_test, daemon=True)
        thread.start()

    def get_hostname(self):
        """Obtém o nome do computador"""
        try:
            return socket.gethostname()
        except Exception as e:
            print(f"Erro ao obter hostname: {e}")
            return "Desconhecido"

    def get_mac_address(self):
        """Obtém o endereço MAC"""
        try:
            import uuid
            mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
            return ':'.join(mac[i:i+2] for i in range(0, 12, 2)).upper()
        except Exception as e:
            print(f"Erro ao obter MAC: {e}")
            return "Desconhecido"

    def get_all_network_info(self):
        """Retorna todas as informações de rede"""
        self.get_public_ip()
        self.get_location()
        self.check_internet()
        
        return {
            'public_ip': self.public_ip,
            'city': self.city,
            'country': self.country,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'is_online': self.is_online,
            'download_speed': self.internet_down,
            'upload_speed': self.internet_up,
            'hostname': self.get_hostname(),
            'mac_address': self.get_mac_address()
        }


# Instância global
network = NetworkMonitor()
