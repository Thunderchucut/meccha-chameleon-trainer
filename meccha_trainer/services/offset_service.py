"""Resolves game-build offsets from offsets/*.json."""
from __future__ import annotations

import json
from pathlib import Path

from meccha_trainer.utils.logging import get_logger

log = get_logger(__name__)
OFFSETS_DIR = Path(__file__).resolve().parents[2] / "offsets"


class OffsetService:
    def __init__(self, build: str) -> None:
        self.build = build
        self._table: dict[str, int] = {}

    def load(self) -> dict[str, int]:
        path = OFFSETS_DIR / f"{self.build}.json"
        if not path.exists():
            log.warning("offsets.missing", build=self.build)
            return {}
        with path.open("r", encoding="utf-8") as fh:
            data = json.load(fh)
        self._table = {k: int(v) for k, v in data.items() if isinstance(v, (int, str))}
        log.info("offsets.loaded", build=self.build, count=len(self._table))
        return self._table

    def resolve(self, name: str) -> int | None:
        return self._table.get(name)