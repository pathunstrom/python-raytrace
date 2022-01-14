from math import sqrt, pi
from pytest import mark, fixture

from tracer import (
    Sphere,
    point,
    vector,
    Vector,
    Matrix,
    Color,
    Light,
    Material,
)


@fixture
def surface_material():
    return Material()


@fixture
def surface_position():
    return point(0, 0, 0)


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
    normal: Vector = sphere.normal_at(_point)
    assert normal == expected_normal
    assert normal == normal.normalize()


@mark.parametrize(
    "_vector, normal, expected",
    [
        [vector(1, -1, 0), vector(0, 1, 0), vector(1, 1, 0)],
        [vector(0, -1, 0), vector(sqrt(2)/2, sqrt(2)/2, 0), vector(1, 0, 0)]
    ]
)
def test_vector_reflect(_vector, normal, expected):
    assert _vector.reflect(normal) == expected


def test_point_light():
    intensity = Color(1, 1, 1)
    position = point(0, 0, 0)
    light = Light(position, intensity)
    assert light.position == position
    assert light.intensity == intensity


def test_material():
    material = Material()
    assert material.color == Color(1, 1, 1)
    assert material.ambient == 0.1
    assert material.diffuse == 0.9
    assert material.specular == 0.9
    assert material.shininess == 200


def test_sphere_material():
    sphere = Sphere()
    assert sphere.material == Material()


def test_sphere_material_instantiate():
    sphere = Sphere(material=Material(ambient=1))
    assert sphere.material.ambient == 1
    assert sphere.material.diffuse == 0.9
    assert sphere.material.specular == 0.9
    assert sphere.material.shininess == 200


def test_sphere_material_set():
    sphere = Sphere()
    material = Material()
    material.ambient = 1
    sphere.material = material
    assert sphere.material == material


@mark.parametrize(
    "eye_vector, surface_normal, light, in_shadow, expected_color",
    [
        [vector(0, 0, -1), vector(0, 0, -1), Light(point(0, 0, -10), Color(1, 1, 1)), False, Color(1.9, 1.9, 1.9)],
        [vector(0, sqrt(2)/2, sqrt(2)/2), vector(0, 0, -1), Light(point(0, 0, -10), Color(1, 1, 1)), False, Color(1, 1, 1)],
        [vector(0, 0, -1), vector(0, 0, -1), Light(point(0, 10, -10), Color(1, 1, 1)), False, Color(0.7364, 0.7364, 0.7364)],
        [vector(0, -sqrt(2)/2, -sqrt(2)/2), vector(0, 0, -1), Light(point(0, 10, -10), Color(1, 1, 1)), False, Color(1.6364, 1.6364, 1.6364)],
        [vector(0, 0, -1), vector(0, 0, -1), Light(point(0, 0, 10), Color(1, 1, 1)), False, Color(0.1, 0.1, 0.1)],
    ]
)
def test_material_lighting(surface_material, surface_position, eye_vector, surface_normal, light, in_shadow, expected_color):
    assert surface_material.lighting(light, surface_position, eye_vector, surface_normal, in_shadow) == expected_color
