from __future__ import annotations
from pytest import mark

from tracer import Intersection, Intersections, Ray, Sphere, Tuple


@mark.parametrize(
    "origin,expected",
    [
        [Tuple.point(0, 0, -5), Intersections((Intersection(4, Sphere()), Intersection(6, Sphere())))],
        [Tuple.point(0, 1, -5), Intersections((Intersection(5, Sphere()), Intersection(5, Sphere())))],
        [Tuple.point(0, 2, -5), Intersections()],
        [Tuple.point(0, 0, 0), Intersections((Intersection(-1, Sphere()), Intersection(1, Sphere())))],
        [Tuple.point(0, 0, 5), Intersections((Intersection(-6, Sphere()), Intersection(-4, Sphere())))]
    ]
)
def test_sphere_intersection(origin: Tuple, expected: Intersections[Intersection]):
    ray = Ray(origin, Tuple.vector(0, 0, 1))
    sphere = Sphere()
    for i in expected:
        i.hull = sphere  # We need the expected sphere to be the original sphere.
    intersections = sphere.intersects(ray)
    assert len(intersections) == len(expected)
    for intersection, expected_intersection in zip(intersections, expected):
        assert intersection.distance == expected_intersection.distance
        assert intersection.hull == expected_intersection.hull


def test_create_ray():
    origin = Tuple.point(1, 2, 3)
    direction = Tuple.vector(4, 5, 6)
    ray = Ray(origin, direction)
    assert ray.origin == origin
    assert ray.direction == direction


def test_position():
    ray = Ray(Tuple.point(2, 3, 4), Tuple.vector(1, 0, 0))
    assert ray.position(0) == Tuple.point(2, 3, 4)
    assert ray.position(1) == Tuple.point(3, 3, 4)
    assert ray.position(-1) == Tuple.point(1, 3, 4)
    assert ray.position(2.5) == Tuple.point(4.5, 3, 4)


def test_intersection():
    sphere = Sphere()
    intersection = Intersection(3.5, sphere)
    assert intersection.distance == 3.5
    assert intersection.hull == sphere


def test_intersections():
    sphere = Sphere()
    intersection_1 = Intersection(1, sphere)
    intersection_2 = Intersection(2, sphere)
    intersections = Intersections((intersection_1, intersection_2))
    assert len(intersections) == 2
    assert intersections[0].distance == 1
    assert intersections[1].distance == 2
