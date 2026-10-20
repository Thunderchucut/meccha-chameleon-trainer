"""Game entity snapshot used by ESP and aim-assist plugins."""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Vec3:
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0

    def to_screen(self, matrix: tuple[float, ...]) -> tuple[float, float] | None:
        w = matrix[3] * self.x + matrix[7] * self.y + matrix[11] * self.z + matrix[15]
        if w < 0.01:
            return None
        sx = (matrix[0] * self.x + matrix[4] * self.y + matrix[8] * self.z + matrix[12]) / w
        sy = (matrix[1] * self.x + matrix[5] * self.y + matrix[9] * self.z + matrix[13]) / w
        return sx, sy


@dataclass
class Entity:
    address: int
    name: str = ""
    team: int = 0
    health: int = 100
    head: Vec3 = field(default_factory=Vec3)
    origin: Vec3 = field(default_factory=Vec3)
    visible: bool = False

    def is_enemy(self, local_team: int) -> bool:
        return self.team != local_team and self.health > 0