"""
Monitoramento de webcam (opcional) - A.R.G.U.S.
"""

import cv2
import threading
from datetime import datetime


class WebcamMonitor:
    def __init__(self):
        self.camera = None
        self.is_recording = False
        self.frame = None
        self.has_permission = False

    def request_permission(self):
        """Solicita permissão para acessar a webcam"""
        try:
            cap = cv2.VideoCapture(0)
            if cap.isOpened():
                self.has_permission = True
                cap.release()
                return True
            return False
        except Exception as e:
            print(f"Erro ao verificar webcam: {e}")
            return False

    def start_recording(self):
        """Inicia a gravação da webcam"""
        if not self.has_permission:
            return False
        
        try:
            self.camera = cv2.VideoCapture(0)
            self.is_recording = True
            
            # Iniciar thread de captura
            thread = threading.Thread(target=self._capture_loop, daemon=True)
            thread.start()
            
            return True
        except Exception as e:
            print(f"Erro ao iniciar webcam: {e}")
            return False

    def _capture_loop(self):
        """Loop de captura de frames"""
        while self.is_recording and self.camera:
            ret, frame = self.camera.read()
            if ret:
                self.frame = frame
            else:
                break

    def stop_recording(self):
        """Para a gravação"""
        self.is_recording = False
        if self.camera:
            self.camera.release()

    def get_frame(self):
        """Retorna o frame atual"""
        return self.frame

    def save_snapshot(self, filename):
        """Salva um snapshot"""
        if self.frame is not None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            cv2.imwrite(f"assets/{timestamp}_{filename}.jpg", self.frame)
            return True
        return False


# Instância global
webcam = WebcamMonitor()
