"""Monitoramento de rede com cache para não bloquear a interface."""

import socket
import threading
import time
from datetime import datetime

import requests
from speedtest import Speedtest


class NetworkMonitor:
    CACHE_SECONDS = 300

    def __init__(self):
        self.public_ip = "Offline"
        self.city = "---"
        self.country = "---"
        self.latitude = 0
        self.longitude = 0
        self.internet_down = 0
        self.internet_up = 0
        self.is_online = False
        self.last_speed_test = None
        self._last_refresh = 0.0
        self._lock = threading.Lock()

    def check_internet(self) -> bool:
        try:
            requests.get("https://www.google.com/generate_204", timeout=2).raise_for_status()
            self.is_online = True
        except requests.RequestException:
            self.is_online = False
        return self.is_online

    def get_public_ip(self) -> str:
        if not self.is_online:
            return "Offline"
        try:
            response = requests.get("https://api.ipify.org", timeout=3)
            response.raise_for_status()
            self.public_ip = response.text.strip()
        except requests.RequestException:
            self.public_ip = "Offline"
        return self.public_ip

    def get_location(self) -> dict:
        if not self.is_online or self.public_ip == "Offline":
            return self._location_dict()
        try:
            response = requests.get(f"https://ipapi.co/{self.public_ip}/json/", timeout=3)
            response.raise_for_status()
            data = response.json()
            self.city = data.get("city") or "---"
            self.country = data.get("country_name") or "---"
            self.latitude = data.get("latitude") or 0
            self.longitude = data.get("longitude") or 0
        except (requests.RequestException, ValueError):
            pass
        return self._location_dict()

    def _location_dict(self) -> dict:
        return {"city": self.city, "country": self.country, "latitude": self.latitude, "longitude": self.longitude}

    def test_speed(self):
        try:
            st = Speedtest()
            st.get_best_server()
            self.internet_down = round(st.download() / 1_000_000, 2)
            self.internet_up = round(st.upload() / 1_000_000, 2)
            self.last_speed_test = datetime.now()
            return {"download": self.internet_down, "upload": self.internet_up, "timestamp": self.last_speed_test.isoformat()}
        except Exception:
            return None

    def test_speed_async(self, callback=None):
        def run_test():
            result = self.test_speed()
            if callback:
                callback(result)
        threading.Thread(target=run_test, daemon=True).start()

    def get_hostname(self) -> str:
        return socket.gethostname()

    def get_mac_address(self) -> str:
        import uuid
        mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
        return ":".join(mac[i:i + 2] for i in range(0, 12, 2)).upper()

    def get_all_network_info(self, force_refresh: bool = False) -> dict:
        """Retorna dados cacheados; serviços externos rodam no máximo a cada 5 min."""
        with self._lock:
            now = time.monotonic()
            if force_refresh or now - self._last_refresh >= self.CACHE_SECONDS:
                self.check_internet()
                self.get_public_ip()
                self.get_location()
                self._last_refresh = now
            return {
                "public_ip": self.public_ip,
                **self._location_dict(),
                "is_online": self.is_online,
                "download_speed": self.internet_down,
                "upload_speed": self.internet_up,
                "hostname": self.get_hostname(),
                "mac_address": self.get_mac_address(),
            }


network = NetworkMonitor()
