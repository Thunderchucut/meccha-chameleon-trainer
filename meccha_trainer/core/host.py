"""TrainerHost — the tick loop that drives plugins and the overlay."""
from __future__ import annotations

import time

from meccha_trainer.core.contracts import TrainerContext
from meccha_trainer.core.registry import PluginRegistry
from meccha_trainer.services.config_service import ConfigService
from meccha_trainer.services.overlay_service import OverlayService
from meccha_trainer.utils.logging import get_logger

TICK_HZ = 60


class TrainerHost:
    def __init__(self, registry: PluginRegistry, cfg: ConfigService,
                 dry_run: bool = False, overlay_enabled: bool = True) -> None:
        self.registry = registry
        self.cfg = cfg
        self.dry_run = dry_run
        self.overlay = OverlayService(cfg) if overlay_enabled else None
        self._log = get_logger(__name__)
        self._running = False

    def run(self) -> None:
        if self.overlay:
            self.overlay.start()
        ctx = TrainerContext(
            game_build=self.cfg.get("game.build", "2026.3.1"),
            offsets=self.cfg.get("game.offsets", {}),
            overlay=self.overlay,
        )
        self._running = True
        interval = 1.0 / TICK_HZ
        while self._running:
            start = time.perf_counter()
            for plugin in self.registry.all():
                try:
                    plugin.on_tick(ctx)
                except Exception as exc:  # noqa: BLE001
                    self._log.warning("plugin.tick_failed",
                                      name=plugin.PLUGIN_MANIFEST.name, err=str(exc))
            elapsed = time.perf_counter() - start
            time.sleep(max(0.0, interval - elapsed))

    def shutdown(self) -> None:
        self._running = False
        self.registry.unregister_all()
        if self.overlay:
            self.overlay.stop()
        self._log.info("trainer.shutdown")