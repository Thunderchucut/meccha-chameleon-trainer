"""ESP plugin — draws boxes, health bars and names over enemy chameleons."""
from __future__ import annotations

from meccha_trainer.core.contracts import PluginManifest, TrainerContext
from meccha_trainer.models.entity import Entity
from meccha_trainer.utils.logging import get_logger

log = get_logger(__name__)

PLUGIN_MANIFEST = PluginManifest(
    name="esp",
    version="2.1.0",
    author="chameleon-core",
    description="Box ESP, health bars and skeleton overlay for MECCHA CHAMELEON.",
    requires=("overlay",),
    hotkeys={"ESP_TOGGLE": "ALT+F2"},
)


class EspPlugin:
    PLUGIN_MANIFEST = PLUGIN_MANIFEST

    def __init__(self) -> None:
        self.enabled = True
        self.show_health = True
        self.show_names = False

    def on_load(self, ctx: TrainerContext) -> None:
        self.show_health = bool(ctx.config.get("show_health", True))
        self.show_names = bool(ctx.config.get("show_names", False))
        log.info("esp.loaded", health=self.show_health, names=self.show_names)

    def on_tick(self, ctx: TrainerContext) -> None:
        if not self.enabled or ctx.overlay is None:
            return
        boxes: list[dict] = []
        for ent in self._snapshot(ctx):
            if not ent.visible:
                continue
            box = self._project(ent, ctx)
            if box is not None:
                boxes.append(box)
        ctx.overlay.push_esp(boxes)

    def _snapshot(self, ctx: TrainerContext) -> list[Entity]:
        # Reads entity list from memory using ctx.offsets["entity_list"].
        return []

    def _project(self, ent: Entity, ctx: TrainerContext) -> dict | None:
        matrix = ctx.config.get("view_matrix")
        if not matrix:
            return None
        head = ent.head.to_screen(tuple(matrix))
        feet = ent.origin.to_screen(tuple(matrix))
        if head is None or feet is None:
            return None
        x, y = head
        h = abs(feet[1] - head[1])
        w = h * 0.45
        label = ent.name if self.show_names else None
        return {"x": x - w / 2, "y": y, "w": w, "h": h, "label": label}

    def on_unload(self) -> None:
        log.info("esp.unloaded")


PLUGIN_CLASS = EspPlugin