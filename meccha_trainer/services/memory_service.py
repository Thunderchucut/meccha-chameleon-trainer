"""Thin wrapper over pymem for attaching to the MECCHA CHAMELEON client."""
from __future__ import annotations

from typing import Any

from meccha_trainer.services.config_service import ConfigService
from meccha_trainer.utils.logging import get_logger

log = get_logger(__name__)

PROCESS_NAMES = ("MecchaChameleon.exe", "MecchaChameleon-Win64-Shipping.exe")


class MemoryService:
    def __init__(self, handle: Any) -> None:
        self.handle = handle

    @classmethod
    def try_attach(cls, cfg: ConfigService) -> "MemoryService | None":
        if not cfg.get("memory.enabled", True):
            return None
        try:
            import pymem  # imported lazily so dry-run works without the game
        except ImportError:
            log.warning("memory.pymem_missing")
            return None
        for name in PROCESS_NAMES:
            try:
                pm = pymem.Pymem(name)
                log.info("memory.attached", process=name, pid=pm.process_id)
                return cls(pm)
            except pymem.exception.ProcessNotFound:
                continue
        log.warning("memory.process_not_found", tried=PROCESS_NAMES)
        return None

    def read_int(self, address: int) -> int:
        import pymem.process
        return self.handle.read_int(address)

    def write_int(self, address: int, value: int) -> None:
        self.handle.write_int(address, value)