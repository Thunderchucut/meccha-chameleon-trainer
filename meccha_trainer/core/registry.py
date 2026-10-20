"""Plugin registry — tracks loaded plugins and their manifest state."""
from __future__ import annotations

from typing import Iterable

from meccha_trainer.core.contracts import PluginManifest, TrainerPlugin
from meccha_trainer.utils.logging import get_logger

API_VERSION = 1


class PluginRegistry:
    def __init__(self) -> None:
        self._plugins: dict[str, TrainerPlugin] = {}
        self._manifests: dict[str, PluginManifest] = {}
        self._log = get_logger(__name__)

    def register(self, plugin: TrainerPlugin) -> None:
        manifest = plugin.PLUGIN_MANIFEST
        if manifest.api != API_VERSION:
            raise RuntimeError(
                f"plugin {manifest.name} targets api {manifest.api}, host is {API_VERSION}"
            )
        if manifest.name in self._plugins:
            self._log.warning("plugin.duplicate", name=manifest.name)
            return
        self._plugins[manifest.name] = plugin
        self._manifests[manifest.name] = manifest
        self._log.info("plugin.registered", name=manifest.name, version=manifest.version)

    def get(self, name: str) -> TrainerPlugin | None:
        return self._plugins.get(name)

    def all(self) -> Iterable[TrainerPlugin]:
        return list(self._plugins.values())

    def manifests(self) -> Iterable[PluginManifest]:
        return list(self._manifests.values())

    def unregister_all(self) -> None:
        for name, plugin in list(self._plugins.items()):
            try:
                plugin.on_unload()
            except Exception as exc:  # noqa: BLE001
                self._log.error("plugin.unload_failed", name=name, err=str(exc))
        self._plugins.clear()
        self._manifests.clear()