"""TOTP compatível com aplicativos autenticadores (RFC 6238)."""

import base64
import hashlib
import hmac
import json
import secrets
import struct
import time
from pathlib import Path
from typing import Optional
from urllib.parse import quote

SECRET_FILE = Path("database/two_factor.json")


def _ensure_secret_file() -> None:
    SECRET_FILE.parent.mkdir(exist_ok=True)
    if not SECRET_FILE.exists():
        set_secret(generate_secret())


def generate_secret() -> str:
    return base64.b32encode(secrets.token_bytes(20)).decode("ascii").rstrip("=")


def get_secret() -> str:
    _ensure_secret_file()
    with SECRET_FILE.open("r", encoding="utf-8") as handle:
        return json.load(handle).get("secret", "")


def set_secret(secret: str) -> str:
    normalized = secret.replace(" ", "").upper()
    base64.b32decode(normalized + "=" * (-len(normalized) % 8), casefold=True)
    temporary = SECRET_FILE.with_suffix(".tmp")
    temporary.write_text(json.dumps({"secret": normalized}, indent=2), encoding="utf-8")
    temporary.replace(SECRET_FILE)
    return normalized


def generate_qr_code(secret: str, account: str = "local") -> str:
    label = quote(f"A.R.G.U.S.:{account}")
    return f"otpauth://totp/{label}?secret={secret}&issuer=A.R.G.U.S&period=30&digits=6"


def generate_totp_code(secret: Optional[str] = None, timestamp: Optional[int] = None) -> str:
    secret_value = secret or get_secret()
    key = base64.b32decode(secret_value + "=" * (-len(secret_value) % 8), casefold=True)
    counter = struct.pack(">Q", (timestamp if timestamp is not None else int(time.time())) // 30)
    digest = hmac.new(key, counter, hashlib.sha1).digest()
    offset = digest[-1] & 0x0F
    value = struct.unpack(">I", digest[offset:offset + 4])[0] & 0x7FFFFFFF
    return f"{value % 1_000_000:06d}"


def verify_totp_code(secret: str, code: str) -> bool:
    if not code or len(code) != 6 or not code.isdigit():
        return False
    try:
        now = int(time.time())
        return any(hmac.compare_digest(code, generate_totp_code(secret, now + offset)) for offset in (-30, 0, 30))
    except (ValueError, TypeError):
        return False

