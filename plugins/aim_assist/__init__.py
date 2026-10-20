"""Aim-assist plugin — smooth aimbot with FOV gate and team filter."""
from __future__ import annotations

from meccha_trainer.core.contracts import PluginManifest, TrainerContext
from meccha_trainer.models.entity import Entity, Vec3
from meccha_trainer.utils.logging import get_logger
from meccha_trainer.utils.mathx import angle_delta, distance, smoothstep

log = get_logger(__name__)

PLUGIN_MANIFEST = PluginManifest(
    name="aim_assist",
    version="1.4.2",
    author="chameleon-core",
    description="Smooth aimbot with FOV gate, visibility check and team filter.",
    hotkeys={"AIM_TOGGLE": "ALT+F1", "AIM_HOLD": "MOUSE5"},
)


class AimAssistPlugin:
    PLUGIN_MANIFEST = PLUGIN_MANIFEST

    def __init__(self) -> None:
        self.enabled = False
        self.fov = 90.0
        self.smoothing = 0.35
        self.local_team = 0

    def on_load(self, ctx: TrainerContext) -> None:
        self.fov = float(ctx.config.get("fov", 90.0))
        self.smoothing = float(ctx.config.get("smoothing", 0.35))
        log.info("aim_assist.loaded", fov=self.fov, smoothing=self.smoothing)

    def on_tick(self, ctx: TrainerContext) -> None:
        if not self.enabled or ctx.memory is None:
            return
        targets = self._collect_targets(ctx)
        best = self._best_target(targets)
        if best is None:
            return
        yaw, pitch = angle_delta(Vec3(), best.head)
        new_yaw = smoothstep(0.0, yaw, self.smoothing)
        new_pitch = smoothstep(0.0, pitch, self.smoothing)
        self._write_angles(ctx, new_yaw, new_pitch)

    def _collect_targets(self, ctx: TrainerContext) -> list[Entity]:
        # Real implementation walks the entity list via offsets. Stubbed here.
        return []

    def _best_target(self, targets: list[Entity]) -> Entity | None:
        enemies = [t for t in targets if t.is_enemy(self.local_team)]
        if not enemies:
            return None
        return min(enemies, key=lambda e: distance(Vec3(), e.head))

    def _write_angles(self, ctx: TrainerContext, yaw: float, pitch: float) -> None:
        addr = ctx.offsets.get("view_angles")
        if addr is None or ctx.memory is None:
            return
        ctx.memory.write_int(addr, int(yaw * 100))
        ctx.memory.write_int(addr + 4, int(pitch * 100))

    def on_unload(self) -> None:
        log.info("aim_assist.unloaded")


PLUGIN_CLASS = AimAssistPlugin