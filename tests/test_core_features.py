import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from ai import ai
from database import db
from monitor import monitor


def test_monitor_stats_has_consistent_schema():
    stats = monitor.get_all_stats()
    assert {"cpu", "ram", "gpu", "disk", "temperature", "processes", "high_usage_processes"} <= stats.keys()
    assert 0 <= stats["cpu"] <= 100
    assert 0 <= stats["ram"] <= 100


def test_ai_response():
    response = ai.get_response("status")
    assert isinstance(response, str)
    assert response


def test_database_history_is_json_ready():
    assert os.path.exists(db.db_path)
    assert isinstance(db.get_latest_stats(limit=1), list)
