from __future__ import annotations
from pytest import mark

from tracer import Ray, Sphere, Tuple


@mark.parametrize(
    "origin,expected",
    [
        [Tuple.point(0, 0, -5), [4, 6]],
        [Tuple.point(0, 1, -5), [5, 5]],
        [Tuple.point(0, 2, -5), []],
        [Tuple.point(0, 0, 0), [-1, 1]],
        [Tuple.point(0, 0, 5), [-6, -4]]
    ]
)
def test_sphere_intersection(origin: Tuple, expected: list[int | float]):
    ray = Ray(origin, Tuple.vector(0, 0, 1))
    sphere = Sphere()
    intersections = sphere.intersects(ray)
    assert len(intersections) == len(expected)
    for intersection, expected_intersection in zip(intersections, expected):
        assert intersection == expected_intersection
