from math import sqrt, pi
from pytest import mark, fixture

from tracer import (
    point,
    vector,
    Color,
    Light,
    Material,
    WHITE,
    BLACK,
    Vector,
    StripePattern,
)


@fixture
def surface_material():
    return Material()


@fixture
def surface_position():
    return point(0, 0, 0)


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
    intensity = WHITE
    position = point(0, 0, 0)
    light = Light(position, intensity)
    assert light.position == position
    assert light.intensity == intensity


def test_material():
    material = Material()
    assert material.color == WHITE
    assert material.ambient == 0.1
    assert material.diffuse == 0.9
    assert material.specular == 0.9
    assert material.shininess == 200


@mark.parametrize(
    "eye_vector, surface_normal, light, in_shadow, expected_color",
    [
        [vector(0, 0, -1), vector(0, 0, -1), Light(point(0, 0, -10), WHITE), False, Color(1.9, 1.9, 1.9)],
        [vector(0, sqrt(2)/2, sqrt(2)/2), vector(0, 0, -1), Light(point(0, 0, -10), WHITE), False, WHITE],
        [vector(0, 0, -1), vector(0, 0, -1), Light(point(0, 10, -10), WHITE), False, Color(0.7364, 0.7364, 0.7364)],
        [vector(0, -sqrt(2)/2, -sqrt(2)/2), vector(0, 0, -1), Light(point(0, 10, -10), WHITE), False, Color(1.6364, 1.6364, 1.6364)],
        [vector(0, 0, -1), vector(0, 0, -1), Light(point(0, 0, 10), WHITE), False, Color(0.1, 0.1, 0.1)],
    ]
)
def test_material_lighting(
        surface_material, surface_position, eye_vector: Vector, surface_normal: Vector,
        light: Light, in_shadow: bool, expected_color: Color
):
    assert surface_material.lighting(light, surface_position, eye_vector, surface_normal, in_shadow) == expected_color


def test_material_with_pattern():
    material = Material(
        ambient=1,
        diffuse=0,
        specular=0,
        pattern=StripePattern(WHITE, BLACK)
    )

    eye_vector = vector(0, 0, -1)
    normal_vector = vector(0, 0, -1)

    light = Light(point(0, 0, -10), WHITE)

    assert material.lighting(light, point(0.9, 0, 0), eye_vector, normal_vector, False) == WHITE
    assert material.lighting(light, point(1.1, 0, 0), eye_vector, normal_vector, False) == BLACK
