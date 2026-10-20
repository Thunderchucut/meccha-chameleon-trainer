"""Shared contracts every MECCHA CHAMELEON Trainer plugin must satisfy."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol, Any


@dataclass(frozen=True)
class PluginManifest:
    name: str
    version: str
    author: str
    api: int = 1
    description: str = ""
    requires: tuple[str, ...] = ()
    hotkeys: dict[str, str] = field(default_factory=dict)


@dataclass
class TrainerContext:
    """Handed to every plugin on load. Read-only by convention."""
    game_build: str
    offsets: dict[str, int]
    memory: Any | None = None
    overlay: Any | None = None
    config: dict[str, Any] = field(default_factory=dict)


class TrainerPlugin(Protocol):
    PLUGIN_MANIFEST: PluginManifest

    def on_load(self, ctx: TrainerContext) -> None: ...
    def on_tick(self, ctx: TrainerContext) -> None: ...
    def on_unload(self) -> None: ...


class HotkeyHook(Protocol):
    def __call__(self, combo: str) -> None: ...