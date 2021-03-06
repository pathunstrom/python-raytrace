from __future__ import annotations

from math import pi, sqrt
from unittest.mock import Mock

from pytest import mark

from tracer import (
    AbstractHull,
    EPSILON,
    Intersection,
    Intersections,
    Ray,
    Sphere,
    Vector,
    transforms,
    Material,
    Matrix,
    Plane,
    point,
    vector
)


class HullTest(AbstractHull):

    def _normal_at(self, point: Vector) -> Vector:
        x, y, z, _ = point
        return vector(x, y, z)


hull_types = [
    HullTest,
    Sphere,
    Plane,
]


@mark.parametrize(
    "hull_type",
    hull_types
)
def test_hull_has_default_transform(hull_type: type):
    shape = hull_type()
    assert shape.transform == Matrix.identity


@mark.parametrize("hull_type", hull_types)
def test_hull_assign_transform(hull_type: type):
    shape = hull_type()
    shape.transform = transforms.translation(2, 3, 4)
    assert shape.transform == transforms.translation(2, 3, 4)


@mark.parametrize("hull_type", hull_types)
def test_hull_instantiate_with_transform(hull_type: type):
    shape = hull_type(transform=transforms.translation(1, 2, 3))
    assert shape.transform == transforms.translation(1, 2, 3)


@mark.parametrize("hull_type", hull_types)
def test_hull_default_material(hull_type: type):
    shape = hull_type()
    assert shape.material == Material()


@mark.parametrize("hull_type", hull_types)
def test_hull_assign_material(hull_type: type):
    shape = hull_type()
    material = Material(ambient=1)
    shape.material = material
    assert shape.material == material


@mark.parametrize("hull_type", hull_types)
def test_hull_instantiate_with_material(hull_type: type):
    material = Material(ambient=1)
    shape = hull_type(material=material)
    assert shape.material == material


@mark.parametrize("hull_type", hull_types)
def test_hull_intersect_scaled(hull_type: type):
    shape = hull_type(transform=transforms.scaling(2, 2, 2))
    shape._intersects = Mock()
    ray = Ray(point(0, 0, -5), vector(0, 0, 1))
    intersections = shape.intersects(ray)
    shape._intersects.assert_called_once()
    shape._intersects.assert_called_with(Ray(point(0, 0, -2.5), vector(0, 0, 0.5)))


@mark.parametrize("hull_type", hull_types)
def test_hull_intersect_translated(hull_type: type):
    shape = hull_type(transform=transforms.translation(5, 0, 0))
    shape._intersects = Mock()
    ray = Ray(point(0, 0, -5), vector(0, 0, 1))
    _ = shape.intersects(ray)
    shape._intersects.assert_called_once()
    shape._intersects.assert_called_with(Ray(point(-5, 0, -5), vector(0, 0, 1)))


def test_hull_normal_at_translated():
    shape = HullTest(transform=transforms.translation(0, 1, 0))
    assert shape.normal_at(point(0, 1.70711, -0.70711)) == vector(0, 0.70711, -0.70711)


def test_hull_normal_at_transformed():
    shape = HullTest(transform=transforms.rotation_z(pi / 5).scale(1, 0.5, 1))
    assert shape.normal_at(point(0, sqrt(2)/2, -sqrt(2)/2)) == vector(0, 0.97014, -0.24254)


@mark.parametrize(
    "origin,expected",
    [
        [Vector.point(0, 0, -5), Intersections((Intersection(4, Sphere()), Intersection(6, Sphere())))],
        [Vector.point(0, 1, -5), Intersections((Intersection(5, Sphere()), Intersection(5, Sphere())))],
        [Vector.point(0, 2, -5), Intersections()],
        [Vector.point(0, 0, 0), Intersections((Intersection(-1, Sphere()), Intersection(1, Sphere())))],
        [Vector.point(0, 0, 5), Intersections((Intersection(-6, Sphere()), Intersection(-4, Sphere())))],
        [point(0, 0, -5), Intersections((Intersection(4, Sphere()), Intersection(6, Sphere())))],
        [point(0, 1, -5), Intersections((Intersection(5, Sphere()), Intersection(5, Sphere())))],
        [point(0, 2, -5), Intersections()],
        [point(0, 0, 0), Intersections((Intersection(-1, Sphere()), Intersection(1, Sphere())))],
        [point(0, 0, 5), Intersections((Intersection(-6, Sphere()), Intersection(-4, Sphere())))]
    ]
)
def test_sphere__intersection(origin: Vector, expected: Intersections[Intersection]):
    ray = Ray(origin, vector(0, 0, 1))
    sphere = Sphere()
    for i in expected:
        i.hull = sphere  # We need the expected sphere to be the original sphere.
    intersections = sphere._intersects(ray)
    assert len(intersections) == len(expected)
    for intersection, expected_intersection in zip(intersections, expected):
        assert intersection.distance == expected_intersection.distance
        assert intersection.hull == expected_intersection.hull


@mark.parametrize(
    "transform,_point,expected_normal",
    [
        [Matrix.identity, point(1, 0, 0), vector(1, 0, 0)],
        [Matrix.identity, point(0, 1, 0), vector(0, 1, 0)],
        [Matrix.identity, point(0, 0, 1), vector(0, 0, 1)],
        [Matrix.identity, point(sqrt(3) / 3, sqrt(3) / 3, sqrt(3) / 3), vector(sqrt(3) / 3, sqrt(3) / 3, sqrt(3) / 3)],
        [Matrix.identity.translate(0, 1, 0), point(0, 1.70711, -0.70711), vector(0, 1.70711, -0.70711)],
        [Matrix.identity.rotate_z(pi / 5).scale(1, 0.5, 1), point(0, sqrt(2) / 2, -sqrt(2) / 2), vector(0, sqrt(2) / 2, -sqrt(2) / 2)]
    ]
)
def test_sphere_normal_at(transform, _point, expected_normal):
    sphere = Sphere(transform=transform)
    normal: Vector = sphere._normal_at(_point)
    assert normal == expected_normal


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
    ray = Ray(Vector.point(2, 3, 4), Vector.vector(1, 0, 0))
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
    assert not comps.inside


def test_intersection_prepare_computations_inside_hit():
    ray = Ray(point(0, 0, 0), vector(0, 0, 1))
    shape = Sphere()
    intersection = Intersection(1, shape)
    computations = intersection.prepare_computations(ray)
    assert computations.point == point(0, 0, 1)
    assert computations.eye_vector == vector(0, 0, -1)
    assert computations.normal_vector == vector(0, 0, -1)
    assert computations.inside


def test_intersection_prepare_computations_over_point():
    ray = Ray(point(0, 0, -5), vector(0, 0, 1))
    shape = Sphere(
        transform=transforms.translation(0, 0, 1)
    )
    intersection = Intersection(5, shape)
    computations = intersection.prepare_computations(ray)

    assert computations.over_point.z < -EPSILON/2
    assert computations.point.z > computations.over_point.z


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


@mark.parametrize("_input", [point(0, 0, 0), point(10, 0, -10), point(-5, 0, 150)])
def test_plane__normal(_input):
    plane = Plane()
    assert plane._normal_at(_input) == vector(0, 1, 0)


@mark.parametrize(
    "_input,expected",
    [
        [Ray(point(0, 10, 0), vector(0, 0, 1)), Intersections()],
        [Ray(point(0, 0, 0), vector(0, 0, 1)), Intersections()],
        [Ray(point(0, 1, 0), vector(0, -1, 0)), Intersections((Intersection(1, Plane()),))],
        [Ray(point(0, -1, 0), vector(0, 1, 0)), Intersections((Intersection(1, Plane()),))]
    ]
)
def test_plane__intersects(_input: Ray, expected: Intersections[Intersection]):
    plane = Plane()
    intersections = plane._intersects(_input)
    assert intersections == expected
