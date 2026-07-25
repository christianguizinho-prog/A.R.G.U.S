"""Reconhecimento e síntese de voz básica para o A.R.G.U.S."""

import pyttsx3


class VoiceAssistant:
    def __init__(self):
        self.engine = None
        self._initialize()

    def _initialize(self):
        try:
            self.engine = pyttsx3.init()
        except Exception as exc:
            print(f"Erro ao inicializar voz: {exc}")
            self.engine = None

    def speak(self, text: str) -> bool:
        if not self.engine:
            return False
        try:
            self.engine.say(text)
            self.engine.runAndWait()
            return True
        except Exception as exc:
            print(f"Erro ao falar: {exc}")
            return False


voice_assistant = VoiceAssistant()
