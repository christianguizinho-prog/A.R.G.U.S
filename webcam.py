"""Captura de webcam compartilhada pela interface local e página web."""
import os
import threading
from datetime import datetime

try:
    import cv2
except ImportError:
    cv2 = None


class WebcamMonitor:
    def __init__(self):
        self.camera = None
        self.is_recording = False
        self.frame = None
        self.device_index = None
        self._lock = threading.Lock()

    def detect_device_index(self):
        backend = cv2.CAP_DSHOW if os.name == "nt" else cv2.CAP_ANY
        for index in range(2):
            cap = cv2.VideoCapture(index, backend)
            try:
                ok, frame = cap.isOpened() and cap.read()
                if ok and frame is not None:
                    self.device_index = index
                    return True
            finally:
                cap.release()
        return False

    def start_recording(self):
        if self.is_recording:
            return True
        if self.device_index is None and not self.detect_device_index():
            return False
        backend = cv2.CAP_DSHOW if os.name == "nt" else cv2.CAP_ANY
        self.camera = cv2.VideoCapture(self.device_index, backend)
        if not self.camera.isOpened():
            self.camera.release()
            self.camera = None
            return False
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        self.is_recording = True
        threading.Thread(target=self._capture_loop, daemon=True).start()
        return True

    def _capture_loop(self):
        while self.is_recording and self.camera and self.camera.isOpened():
            ok, frame = self.camera.read()
            if not ok:
                self.is_recording = False
                break
            with self._lock:
                self.frame = frame

    def stop_recording(self):
        self.is_recording = False
        if self.camera:
            self.camera.release()
            self.camera = None
        with self._lock:
            self.frame = None

    def get_frame(self):
        with self._lock:
            return None if self.frame is None else self.frame.copy()

    def get_jpeg_frame(self):
        frame = self.get_frame()
        if frame is None:
            return None
        ok, buffer = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
        return buffer.tobytes() if ok else None

    def save_snapshot(self, filename):
        frame = self.get_frame()
        if frame is None:
            return False
        os.makedirs("assets", exist_ok=True)
        return bool(cv2.imwrite("assets/{0}_{1}.jpg".format(datetime.now().strftime("%Y%m%d_%H%M%S"), filename), frame))


webcam = WebcamMonitor()

