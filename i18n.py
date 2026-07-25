"""Suporte bÃ¡sico a mÃºltiplos idiomas para o A.R.G.U.S."""

import json
from pathlib import Path
from typing import Optional

LANGUAGE_FILE = Path("database/language.json")

TRANSLATIONS = {
    "pt-BR": {
        "title": "A.R.G.U.S. v3.1",
        "login_title": "Acesso ao A.R.G.U.S.",
        "username": "UsuÃ¡rio",
        "password": "Senha",
        "login": "Entrar",
        "register": "Registrar",
        "fullscreen": "Tela cheia",
        "language": "Idioma",
        "api_start": "Iniciar API",
        "api_stop": "Parar API",
        "export_pdf": "Exportar PDF",
        "export_excel": "Exportar Excel",
        "notify_test": "Testar notificaÃ§Ã£o",
        "cleanup": "Executar limpeza",
        "backup": "Backup",
        "speak": "Falar resposta",
        "plugin": "Executar plugins",
        "status_normal": "Status: Normal",
        "status_alert": "Status: Alerta",
        "api_online": "API online",
        "api_offline": "API offline",
        "report_saved": "RelatÃ³rio salvo",
        "backup_done": "Backup realizado",
        "cleanup_done": "Limpeza concluÃ­da",
        "voice_error": "Falha no Ã¡udio",
        "language_saved": "Idioma salvo",
        "login_failed": "Falha na autenticaÃ§Ã£o",
    },
    "en-US": {
        "title": "A.R.G.U.S. v3.1",
        "login_title": "A.R.G.U.S. Access",
        "username": "Username",
        "password": "Password",
        "login": "Login",
        "register": "Register",
        "fullscreen": "Fullscreen",
        "language": "Language",
        "api_start": "Start API",
        "api_stop": "Stop API",
        "export_pdf": "Export PDF",
        "export_excel": "Export Excel",
        "notify_test": "Test notification",
        "cleanup": "Run cleanup",
        "backup": "Backup",
        "speak": "Speak response",
        "plugin": "Run plugins",
        "status_normal": "Status: Normal",
        "status_alert": "Status: Alert",
        "api_online": "API online",
        "api_offline": "API offline",
        "report_saved": "Report saved",
        "backup_done": "Backup completed",
        "cleanup_done": "Cleanup completed",
        "voice_error": "Audio failed",
        "language_saved": "Language saved",
        "login_failed": "Authentication failed",
    },
}


def _ensure_language_file():
    LANGUAGE_FILE.parent.mkdir(exist_ok=True)
    if not LANGUAGE_FILE.exists():
        LANGUAGE_FILE.write_text(json.dumps({"language": "pt-BR"}), encoding="utf-8")
    return LANGUAGE_FILE


def get_current_language() -> str:
    try:
        _ensure_language_file()
        with LANGUAGE_FILE.open("r", encoding="utf-8") as handle:
            return json.load(handle).get("language", "pt-BR")
    except Exception:
        return "pt-BR"


def set_language(language: str) -> str:
    _ensure_language_file()
    with LANGUAGE_FILE.open("w", encoding="utf-8") as handle:
        json.dump({"language": language}, handle, indent=2)
    return language


def get_text(key: str, language: Optional[str] = None) -> str:
    lang = language or get_current_language()
    return TRANSLATIONS.get(lang, TRANSLATIONS["pt-BR"]).get(key, key)

