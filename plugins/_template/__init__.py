"""Copy this folder to start a new MECCHA CHAMELEON Trainer plugin."""
from __future__ import annotations

from meccha_trainer.core.contracts import PluginManifest, TrainerContext
from meccha_trainer.utils.logging import get_logger

log = get_logger(__name__)

PLUGIN_MANIFEST = PluginManifest(
    name="template",
    version="0.0.1",
    author="you",
    description="Starter plugin — rename me.",
)


class TemplatePlugin:
    PLUGIN_MANIFEST = PLUGIN_MANIFEST

    def on_load(self, ctx: TrainerContext) -> None:
        log.info("template.loaded", build=ctx.game_build)

    def on_tick(self, ctx: TrainerContext) -> None:
        pass

    def on_unload(self) -> None:
        pass


PLUGIN_CLASS = TemplatePlugin