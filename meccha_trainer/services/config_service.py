"""YAML config loader with dotted-path accessors."""
from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


class ConfigService:
    def __init__(self, data: dict[str, Any]) -> None:
        self._data = data or {}

    @classmethod
    def load(cls, path: str | Path) -> "ConfigService":
        p = Path(path)
        if not p.exists():
            return cls({})
        with p.open("r", encoding="utf-8") as fh:
            return cls(yaml.safe_load(fh) or {})

    def get(self, dotted: str, default: Any = None) -> Any:
        cur: Any = self._data
        for part in dotted.split("."):
            if not isinstance(cur, dict) or part not in cur:
                return default
            cur = cur[part]
        return cur

    def section(self, name: str) -> dict[str, Any]:
        val = self.get(f"plugins.{name}", {})
        return val if isinstance(val, dict) else {}