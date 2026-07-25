"""Plugins locais com manifesto, validação e ativação explícita.

Plugins são código Python: instale apenas plugins confiáveis.
"""

import importlib.util
import json
from pathlib import Path
from typing import Any, Dict, List

PLUGIN_DIR = Path("plugins")
PLUGIN_CONFIG = Path("database/plugins.json")
API_VERSION = "1.0"


def _load_settings() -> Dict[str, Any]:
    PLUGIN_CONFIG.parent.mkdir(exist_ok=True)
    if not PLUGIN_CONFIG.exists():
        PLUGIN_CONFIG.write_text(json.dumps({"enabled": []}, indent=2), encoding="utf-8")
    return json.loads(PLUGIN_CONFIG.read_text(encoding="utf-8"))


def _manifest(plugin_path: Path) -> Dict[str, Any]:
    manifest_path = plugin_path.with_suffix(".json")
    if not manifest_path.exists():
        return {"name": plugin_path.stem, "version": "0.0.0", "api_version": API_VERSION, "description": "Plugin legado"}
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    required = {"name", "version", "api_version"}
    if not required <= data.keys() or data["api_version"] != API_VERSION:
        raise ValueError("manifesto inválido ou incompatível")
    return data


def list_plugins() -> List[Dict[str, Any]]:
    PLUGIN_DIR.mkdir(exist_ok=True)
    enabled = set(_load_settings().get("enabled", []))
    items = []
    for path in sorted(PLUGIN_DIR.glob("*.py")):
        if path.name.startswith("_"):
            continue
        try:
            data = _manifest(path)
            data.update({"id": path.stem, "enabled": path.stem in enabled, "valid": True})
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            data = {"id": path.stem, "enabled": False, "valid": False, "error": str(exc)}
        items.append(data)
    return items


def set_plugin_enabled(plugin_id: str, enabled: bool) -> bool:
    available = {item["id"] for item in list_plugins() if item["valid"]}
    if plugin_id not in available:
        return False
    settings = _load_settings()
    values = set(settings.get("enabled", []))
    values.add(plugin_id) if enabled else values.discard(plugin_id)
    PLUGIN_CONFIG.write_text(json.dumps({"enabled": sorted(values)}, indent=2), encoding="utf-8")
    return True


def load_plugins() -> List[Dict[str, Any]]:
    loaded = []
    for item in list_plugins():
        if not item["valid"] or not item["enabled"]:
            continue
        path = PLUGIN_DIR / (item["id"] + ".py")
        try:
            spec = importlib.util.spec_from_file_location("argus_plugin_" + item["id"], path)
            if not spec or not spec.loader:
                raise ImportError("não foi possível carregar o plugin")
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            if not callable(getattr(module, "run", None)):
                raise ValueError("plugin não expõe run(context)")
            loaded.append({"metadata": item, "module": module})
        except Exception as exc:
            loaded.append({"metadata": item, "error": str(exc)})
    return loaded


def run_plugins(context: Dict[str, Any] = None) -> List[str]:
    results = []
    for plugin in load_plugins():
        meta = plugin["metadata"]
        if "error" in plugin:
            results.append("{0}: erro - {1}".format(meta["name"], plugin["error"]))
            continue
        try:
            results.append("{0}: {1}".format(meta["name"], plugin["module"].run(context or {})))
        except Exception as exc:
            results.append("{0}: erro - {1}".format(meta["name"], exc))
    return results
