"""Notificações desktop com sinal sonoro opcional e falha silenciosa."""

import os
from typing import Optional

try:
    from plyer import notification
except ImportError:
    notification = None


def _play_alert_sound() -> None:
    if os.name == "nt":
        try:
            import winsound
            winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
        except RuntimeError:
            pass
    else:
        print("\a", end="", flush=True)


def send_notification(title: str, message: str, timeout: int = 5, sound: bool = True) -> bool:
    if sound:
        _play_alert_sound()
    if notification is None:
        return False
    try:
        notification.notify(title=title, message=message, app_name="A.R.G.U.S.", timeout=timeout)
        return True
    except Exception:
        return False
