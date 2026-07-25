"""Previsões leves baseadas no histórico local, sem dependências de ML externas."""

from typing import Dict, Iterable, List, Optional


def linear_forecast(values: Iterable[float], steps: int = 5) -> List[float]:
    data = [float(value) for value in values]
    if not data:
        return []
    if len(data) == 1:
        return [round(data[0], 2)] * steps
    mean_x = (len(data) - 1) / 2
    mean_y = sum(data) / len(data)
    denominator = sum((index - mean_x) ** 2 for index in range(len(data)))
    slope = sum((index - mean_x) * (value - mean_y) for index, value in enumerate(data)) / denominator
    intercept = mean_y - slope * mean_x
    return [round(min(100.0, max(0.0, intercept + slope * (len(data) + index))), 2) for index in range(steps)]


def predict_from_history(history: List[Dict[str, object]], steps: int = 5) -> Dict[str, List[float]]:
    mappings = {"cpu": "cpu_usage", "ram": "ram_usage", "disk": "disk_usage", "temperature": "temperature"}
    ordered = list(reversed(history))
    return {name: linear_forecast([row[column] for row in ordered if row.get(column) is not None], steps) for name, column in mappings.items()}
