from math import sqrt, pi
from pytest import mark

from tracer import Sphere, point, vector, Tuple, Matrix


@mark.parametrize(
    "transform,_point,expected_normal",
    [
        [Matrix.identity, point(1, 0, 0), vector(1, 0, 0)],
        [Matrix.identity, point(0, 1, 0), vector(0, 1, 0)],
        [Matrix.identity, point(0, 0, 1), vector(0, 0, 1)],
        [Matrix.identity, point(sqrt(3) / 3, sqrt(3) / 3, sqrt(3) / 3), vector(sqrt(3) / 3, sqrt(3) / 3, sqrt(3) / 3)],
        [Matrix.identity.translate(0, 1, 0), point(0, 1.70711, -0.70711), vector(0, 0.70711, -0.70711)],
        [Matrix.identity.rotate_z(pi / 5).scale(1, 0.5, 1), point(0, sqrt(2) / 2, -sqrt(2) / 2), vector(0, 0.97014, -0.24254)]
    ]
)
def test_sphere_normal_at(transform, _point, expected_normal):
    sphere = Sphere(transform=transform)
    normal: Tuple = sphere.normal_at(_point)
    assert normal == expected_normal
    assert normal == normal.normalize()
