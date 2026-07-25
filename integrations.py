"""Integrações opt-in com Telegram, Discord e backups locais/WebDAV."""
import json
import shutil
from pathlib import Path
from typing import Any, Dict
from urllib.parse import quote, urlparse
import requests

CONFIG_FILE = Path("database/integrations.json")

def _defaults() -> Dict[str, Any]:
    return {"telegram": {"enabled": False, "token": "", "chat_id": ""}, "discord": {"enabled": False, "webhook": ""}, "cloud": {"enabled": False, "provider": "local", "folder": "database/cloud_backup", "webdav_url": "", "username": "", "password": ""}}

def _ensure_config() -> None:
    CONFIG_FILE.parent.mkdir(exist_ok=True)
    if not CONFIG_FILE.exists(): CONFIG_FILE.write_text(json.dumps(_defaults(), indent=2), encoding="utf-8")

def load_config() -> Dict[str, Any]:
    _ensure_config(); data = _defaults()
    try:
        for section, values in json.loads(CONFIG_FILE.read_text(encoding="utf-8")).items():
            if isinstance(values, dict) and section in data: data[section].update(values)
    except (OSError, json.JSONDecodeError): pass
    return data

def save_config(data: Dict[str, Any]) -> Dict[str, Any]:
    merged = _defaults()
    for section, values in data.items():
        if isinstance(values, dict) and section in merged: merged[section].update(values)
    temporary = CONFIG_FILE.with_suffix(".tmp"); temporary.write_text(json.dumps(merged, indent=2), encoding="utf-8"); temporary.replace(CONFIG_FILE)
    return merged

def send_telegram_message(message: str) -> bool:
    config = load_config()["telegram"]
    if not config["enabled"] or not config["token"] or not config["chat_id"]: return False
    try: return requests.post("https://api.telegram.org/bot{0}/sendMessage".format(config["token"]), data={"chat_id": config["chat_id"], "text": message}, timeout=5).ok
    except requests.RequestException: return False

def send_discord_message(message: str) -> bool:
    config = load_config()["discord"]
    if not config["enabled"] or not config["webhook"]: return False
    try: return requests.post(config["webhook"], json={"content": message}, timeout=5).ok
    except requests.RequestException: return False

def trigger_integrations(message: str) -> Dict[str, bool]: return {"telegram": send_telegram_message(message), "discord": send_discord_message(message)}

def sync_to_cloud() -> Dict[str, str]:
    cloud = load_config()["cloud"]
    if not cloud["enabled"]: return {"status": "disabled"}
    source = Path("database/logs.db")
    if not source.exists(): return {"status": "missing_source"}
    provider = cloud.get("provider", "local")
    if provider == "local":
        destination_dir = Path(cloud.get("folder", "database/cloud_backup")); destination_dir.mkdir(parents=True, exist_ok=True)
        destination = destination_dir / source.name; shutil.copy2(source, destination)
        return {"status": "ok", "provider": "local", "path": str(destination)}
    if provider != "webdav": return {"status": "invalid_provider"}
    endpoint = cloud.get("webdav_url", "").rstrip("/") + "/" + quote(source.name)
    parsed = urlparse(endpoint)
    if parsed.scheme != "https" or not parsed.netloc: return {"status": "invalid_webdav_url"}
    try:
        with source.open("rb") as handle: response = requests.put(endpoint, data=handle, auth=(cloud.get("username", ""), cloud.get("password", "")), timeout=30)
        return {"status": "ok", "provider": "webdav", "path": endpoint} if response.ok else {"status": "remote_error", "code": str(response.status_code)}
    except requests.RequestException: return {"status": "network_error"}
