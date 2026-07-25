"""Gerenciamento simples de tema e preferências visuais."""

import json
from pathlib import Path

THEME_FILE = Path("database/theme.json")


def _ensure_theme_file():
    THEME_FILE.parent.mkdir(exist_ok=True)
    if not THEME_FILE.exists():
        THEME_FILE.write_text(json.dumps({"theme": "dark"}), encoding="utf-8")
    return THEME_FILE


def get_theme_preference() -> str:
    try:
        _ensure_theme_file()
        with THEME_FILE.open("r", encoding="utf-8") as handle:
            return json.load(handle).get("theme", "dark")
    except Exception:
        return "dark"


def set_theme_preference(theme: str) -> str:
    _ensure_theme_file()
    with THEME_FILE.open("w", encoding="utf-8") as handle:
        json.dump({"theme": theme}, handle, indent=2)
    return theme
