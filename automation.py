"""Automação básica para o A.R.G.U.S."""

import shutil
from datetime import datetime
from pathlib import Path

from database import db


def cleanup_temp_files(root: str = ".") -> dict:
    """Remove diretórios temporários comuns e cache de Python."""
    removed = []
    base = Path(root)
    for candidate in [base / "__pycache__", base / ".pytest_cache", base / "build", base / "dist"]:
        if candidate.exists():
            shutil.rmtree(candidate, ignore_errors=True)
            removed.append(str(candidate))
    return {"removed": removed, "count": len(removed)}


def create_backup(destination_dir: str = "database/backups") -> dict:
    """Cria um backup simples do banco de dados."""
    destination = Path(destination_dir)
    destination.mkdir(parents=True, exist_ok=True)
    from config import DB_PATH

    source_path = Path(DB_PATH)
    if not source_path.exists():
        return {"status": "error", "path": None}

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = destination / f"{source_path.stem}_{timestamp}.db"
    shutil.copy2(source_path, backup_path)
    db.log_alert("BACKUP", f"Backup criado em {backup_path}", "NORMAL")
    return {"status": "ok", "path": str(backup_path)}


def run_automation_tasks() -> dict:
    """Executa conjunto básico de automações."""
    cleanup = cleanup_temp_files()
    backup = create_backup()
    return {"cleanup": cleanup, "backup": backup}
