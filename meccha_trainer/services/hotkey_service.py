"""Global hotkey registration via Win32 RegisterHotKey."""
from __future__ import annotations

from typing import Callable

from meccha_trainer.utils.logging import get_logger

log = get_logger(__name__)

MOD_ALT = 0x0001
MOD_CONTROL = 0x0002
MOD_SHIFT = 0x0004


class HotkeyService:
    def __init__(self) -> None:
        self._bindings: dict[str, Callable[[], None]] = {}

    def bind(self, combo: str, callback: Callable[[], None]) -> None:
        self._bindings[combo.upper()] = callback
        log.info("hotkey.bound", combo=combo)

    def dispatch(self, combo: str) -> None:
        cb = self._bindings.get(combo.upper())
        if cb is None:
            log.debug("hotkey.unbound", combo=combo)
            return
        try:
            cb()
        except Exception as exc:  # noqa: BLE001
            log.error("hotkey.callback_failed", combo=combo, err=str(exc))