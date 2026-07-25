import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import api_server
import auth
from two_factor import generate_secret, generate_totp_code, generate_qr_code, verify_totp_code


def test_password_registration_and_authentication(tmp_path, monkeypatch):
    monkeypatch.setattr(auth, "AUTH_PATH", tmp_path / "auth.json")
    assert auth.register_user("operator", "uma-senha-segura")
    assert auth.authenticate_user("operator", "uma-senha-segura")
    assert not auth.authenticate_user("operator", "senha-errada")
    assert not auth.register_user("weak", "curta")


def test_totp_is_standard_and_verifiable():
    secret = generate_secret()
    code = generate_totp_code(secret)
    assert verify_totp_code(secret, code)
    assert generate_qr_code(secret).startswith("otpauth://totp/")


def test_api_requires_token_and_returns_stats(tmp_path, monkeypatch):
    monkeypatch.setattr(api_server, "TOKEN_FILE", tmp_path / "api_token.txt")
    token = api_server.get_api_token()
    client = api_server.app.test_client()
    assert client.get("/api/stats").status_code == 401
    response = client.get("/api/stats", headers={"X-API-Key": token})
    assert response.status_code == 200
    assert "cpu" in response.get_json()

