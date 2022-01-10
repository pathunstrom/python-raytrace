from __future__ import annotations

from pytest import mark

from tracer import (
    Intersection,
    Intersections,
    Ray,
    Sphere,
    Tuple,
    transforms,
    Matrix,
    point,
    vector
)


@mark.parametrize(
    "origin,expected",
    [
        [Tuple.point(0, 0, -5), Intersections((Intersection(4, Sphere()), Intersection(6, Sphere())))],
        [Tuple.point(0, 1, -5), Intersections((Intersection(5, Sphere()), Intersection(5, Sphere())))],
        [Tuple.point(0, 2, -5), Intersections()],
        [Tuple.point(0, 0, 0), Intersections((Intersection(-1, Sphere()), Intersection(1, Sphere())))],
        [Tuple.point(0, 0, 5), Intersections((Intersection(-6, Sphere()), Intersection(-4, Sphere())))],
        [point(0, 0, -5), Intersections((Intersection(4, Sphere()), Intersection(6, Sphere())))],
        [point(0, 1, -5), Intersections((Intersection(5, Sphere()), Intersection(5, Sphere())))],
        [point(0, 2, -5), Intersections()],
        [point(0, 0, 0), Intersections((Intersection(-1, Sphere()), Intersection(1, Sphere())))],
        [point(0, 0, 5), Intersections((Intersection(-6, Sphere()), Intersection(-4, Sphere())))]
    ]
)
def test_sphere_intersection(origin: Tuple, expected: Intersections[Intersection]):
    ray = Ray(origin, vector(0, 0, 1))
    sphere = Sphere()
    for i in expected:
        i.hull = sphere  # We need the expected sphere to be the original sphere.
    intersections = sphere.intersects(ray)
    assert len(intersections) == len(expected)
    for intersection, expected_intersection in zip(intersections, expected):
        assert intersection.distance == expected_intersection.distance
        assert intersection.hull == expected_intersection.hull


def test_create_ray():
    origin = point(1, 2, 3)
    direction = vector(4, 5, 6)
    ray = Ray(origin, direction)
    assert ray.origin == origin
    assert ray.direction == direction


@mark.parametrize(
    "ray,transform,expected_ray",
    [
        [Ray(point(1, 2, 3), vector(0, 1, 0)), transforms.translation(3, 4, 5), Ray(point(4, 6, 8), vector(0, 1, 0))],
        [Ray(point(1, 2, 3), vector(0, 1, 0)), transforms.scaling(2, 3, 4), Ray(point(2, 6, 12), vector(0, 3, 0))]
    ]
)
def test_ray_transform(ray: Ray, transform: Matrix, expected_ray: Ray):
    result: Ray = ray.transform(transform)
    assert result.origin == expected_ray.origin
    assert result.direction == expected_ray.direction


def test_ray_position():
    ray = Ray(Tuple.point(2, 3, 4), Tuple.vector(1, 0, 0))
    assert ray.position(0) == point(2, 3, 4)
    assert ray.position(1) == point(3, 3, 4)
    assert ray.position(-1) == point(1, 3, 4)
    assert ray.position(2.5) == point(4.5, 3, 4)


def test_intersection():
    sphere = Sphere()
    intersection = Intersection(3.5, sphere)
    assert intersection.distance == 3.5
    assert intersection.hull == sphere


def test_intersection_prepare_computations():
    ray = Ray(point(0, 0, -5), vector(0, 0, 1))
    shape = Sphere()
    intersection = Intersection(4, shape)
    comps = intersection.prepare_computations(ray)

    assert comps.distance == intersection.distance
    assert comps.hull == intersection.hull
    assert comps.point == point(0, 0, -1)
    assert comps.eye_vector == vector(0, 0, -1)
    assert comps.normal_vector == vector(0, 0, -1)


def test_intersections():
    sphere = Sphere()
    intersection_1 = Intersection(1, sphere)
    intersection_2 = Intersection(2, sphere)
    intersections = Intersections((intersection_1, intersection_2))
    assert len(intersections) == 2
    assert intersections[0].distance == 1
    assert intersections[1].distance == 2


@mark.parametrize(
    "distances, expected_index",
    [
        [[1, 2], 0],
        [[-1, 1], 1],
        [[-2, -1], None],
        [[5, 7, -3, 2], 3]
    ]
)
def test_intersections_hit(distances, expected_index: int):
    sphere = Sphere()
    intersections = Intersections(Intersection(distance, sphere) for distance in distances)
    hit = intersections.hit()
    if expected_index is None:
        assert hit is None
    else:
        assert intersections[expected_index] is hit


@mark.parametrize(
    "transform, expected",
    [
        [transforms.scaling(2, 2, 2), Intersections((Intersection(3, Sphere()), Intersection(7, Sphere())))],
        [transforms.translation(5, 0, 0), Intersections()]
    ]
)
def test_intersections_transformed(transform: Matrix, expected: Intersections[Intersection]):
    ray = Ray(point(0, 0, -5), vector(0, 0, 1))
    sphere = Sphere(transform=transform)
    for i in expected:
        i.hull = sphere
    intersections = sphere.intersects(ray)
    assert len(intersections) == len(expected)
    for actual, expected in zip(intersections, expected):
        assert actual == expected


def test_sphere_default_transform():
    assert Sphere().transform == Matrix.identity


def test_sphere_change_transform():
    transform = transforms.translation(2, 3, 4)
    sphere = Sphere()
    sphere.transform = transform
    assert sphere.transform == transform


def test_sphere_initialize_transform():
    transform = transforms.shearing(1, 2, 3, 4, 5, 6)
    sphere = Sphere(transform=transform)
    assert sphere.transform == transform


