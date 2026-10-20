import math

from meccha_trainer.models.entity import Vec3
from meccha_trainer.utils.mathx import angle_delta, distance, smoothstep


def test_distance_axis():
    assert distance(Vec3(0, 0, 0), Vec3(3, 4, 0)) == 5.0


def test_angle_delta_yaw():
    yaw, pitch = angle_delta(Vec3(), Vec3(10, 0, 0))
    assert math.isclose(yaw, 0.0, abs_tol=1e-6)
    assert math.isclose(pitch, 0.0, abs_tol=1e-6)


def test_smoothstep_midpoint():
    assert smoothstep(0.0, 10.0, 0.5) == 5.0
    assert smoothstep(0.0, 10.0, 2.0) == 10.0  # clamped
</final_file>