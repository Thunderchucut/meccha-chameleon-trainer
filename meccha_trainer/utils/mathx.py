"""Small vector/matrix helpers for aimbot math."""
from __future__ import annotations

import math

from meccha_trainer.models.entity import Vec3


def distance(a: Vec3, b: Vec3) -> float:
    return math.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2 + (a.z - b.z) ** 2)


def angle_delta(src: Vec3, dst: Vec3) -> tuple[float, float]:
    dx, dy, dz = dst.x - src.x, dst.y - src.y, dst.z - src.z
    yaw = math.degrees(math.atan2(dy, dx))
    pitch = math.degrees(math.atan2(dz, math.hypot(dx, dy)))
    return yaw, pitch


def clamp(v: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, v))


def smoothstep(current: float, target: float, factor: float) -> float:
    factor = clamp(factor, 0.0, 1.0)
    return current + (target - current) * factor