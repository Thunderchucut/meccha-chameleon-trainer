"""Discovers and loads plugin packages from the plugins/ directory."""
from __future__ import annotations

import importlib
import pkgutil
from pathlib import Path

from meccha_trainer.core.contracts import TrainerContext, TrainerPlugin
from meccha_trainer.core.registry import PluginRegistry
from meccha_trainer.services.config_service import ConfigService
from meccha_trainer.services.memory_service import MemoryService
from meccha_trainer.utils.logging import get_logger

PLUGINS_ROOT = Path(__file__).resolve().parents[2] / "plugins"


class PluginLoader:
    def __init__(self, registry: PluginRegistry, cfg: ConfigService) -> None:
        self.registry = registry
        self.cfg = cfg
        self._log = get_logger(__name__)
        self._forced: set[str] = set()

    def discover(self) -> None:
        if not PLUGINS_ROOT.exists():
            self._log.warning("plugins.root_missing", path=str(PLUGINS_ROOT))
            return
        for mod in pkgutil.iter_modules([str(PLUGINS_ROOT)]):
            if mod.name.startswith("_"):
                continue
            self._load_module(f"plugins.{mod.name}")

    def force_enable(self, name: str) -> None:
        self._forced.add(name)
        self._load_module(f"plugins.{name}")

    def _load_module(self, dotted: str) -> None:
        try:
            mod = importlib.import_module(dotted)
        except Exception as exc:  # noqa: BLE001
            self._log.error("plugin.import_failed", module=dotted, err=str(exc))
            return
        plugin_cls = getattr(mod, "PLUGIN_CLASS", None)
        if plugin_cls is None:
            self._log.debug("plugin.no_class", module=dotted)
            return
        plugin: TrainerPlugin = plugin_cls()
        self.registry.register(plugin)
        ctx = TrainerContext(
            game_build=self.cfg.get("game.build", "2026.3.1"),
            offsets=self.cfg.get("game.offsets", {}),
            memory=MemoryService.try_attach(self.cfg),
            config=self.cfg.section(plugin.PLUGIN_MANIFEST.name),
        )
        try:
            plugin.on_load(ctx)
        except Exception as exc:  # noqa: BLE001
            self._log.error("plugin.load_failed", name=plugin.PLUGIN_MANIFEST.name, err=str(exc))