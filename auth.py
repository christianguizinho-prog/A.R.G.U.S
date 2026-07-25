"""Autenticação local segura para o A.R.G.U.S.

Os dados ficam fora do controle de versão em ``database/auth.json``. Não há
usuário ou senha padrão: o primeiro usuário é criado na tela de acesso.
"""

import hashlib
import hmac
import json
import os
from pathlib import Path

AUTH_PATH = Path("database/auth.json")
ITERATIONS = 310_000
MIN_PASSWORD_LENGTH = 12


def _ensure_auth_file() -> Path:
    AUTH_PATH.parent.mkdir(exist_ok=True)
    if not AUTH_PATH.exists():
        AUTH_PATH.write_text(json.dumps({"users": {}}, indent=2), encoding="utf-8")
    return AUTH_PATH


def _load_users() -> dict:
    _ensure_auth_file()
    with AUTH_PATH.open("r", encoding="utf-8") as handle:
        return json.load(handle).get("users", {})


def _save_users(users: dict) -> None:
    temporary = AUTH_PATH.with_suffix(".tmp")
    temporary.write_text(json.dumps({"users": users}, indent=2), encoding="utf-8")
    temporary.replace(AUTH_PATH)


def _password_record(password: str) -> dict:
    salt = os.urandom(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, ITERATIONS)
    return {"algorithm": "pbkdf2_sha256", "iterations": ITERATIONS, "salt": salt.hex(), "hash": digest.hex()}


def _matches(password: str, record: object) -> bool:
    if not isinstance(record, dict) or record.get("algorithm") != "pbkdf2_sha256":
        return False
    try:
        actual = hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), bytes.fromhex(record["salt"]), int(record["iterations"])
        ).hex()
        return hmac.compare_digest(actual, record["hash"])
    except (KeyError, TypeError, ValueError):
        return False


def password_is_valid(password: str) -> bool:
    return len(password) >= MIN_PASSWORD_LENGTH


def authenticate_user(username: str, password: str) -> bool:
    """Valida credenciais sem registrar senhas ou detalhes sensíveis."""
    try:
        return _matches(password, _load_users().get(username))
    except (OSError, json.JSONDecodeError):
        return False


def register_user(username: str, password: str) -> bool:
    """Cria um usuário local; nomes vazios e senhas fracas são rejeitados."""
    username = username.strip()
    if not username or len(username) > 64 or not password_is_valid(password):
        return False
    try:
        users = _load_users()
        if username in users and isinstance(users[username], dict):
            return False
        users[username] = _password_record(password)
        _save_users(users)
        return True
    except (OSError, json.JSONDecodeError):
        return False


def change_password(username: str, old_password: str, new_password: str) -> bool:
    if not password_is_valid(new_password) or not authenticate_user(username, old_password):
        return False
    users = _load_users()
    users[username] = _password_record(new_password)
    _save_users(users)
    return True



