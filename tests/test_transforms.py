"""
Test tracer transforms.

Transforms are helper methods for creating Matrix objects.
"""
from math import pi, sqrt

from pytest import mark

from tracer import transforms, Tuple, Matrix


def test_translation():
    transform = transforms.translation(5, -3, 2)
    inverse = transform.inverse()
    point = Tuple.point(-3, 4, 5)

    assert transform * point == Tuple.point(2, 1, 7)
    assert inverse * point == Tuple.point(-8, 7, 3)


def test_translation_no_effect_on_vectors():
    transform = transforms.translation(5, -3, 2)
    vector = Tuple.vector(-3, 4, 5)

    assert transform * vector == vector


def test_scaling():
    transform = transforms.scaling(2, 3, 4)
    point = Tuple.point(-4, 6, 8)
    vector = Tuple.vector(-4, 6, 8)
    inverse = transform.inverse()

    assert transform * point == Tuple.point(-8, 18, 32)
    assert inverse * point == Tuple.point(-2, 2, 2)
    assert transform * vector == Tuple.vector(-8, 18, 32)


def test_reflection():
    transform = transforms.scaling(-1, 1, 1)
    point = Tuple.point(2, 3, 4)

    assert transform * point == Tuple.point(-2, 3, 4)


def test_rotation_x():
    point = Tuple.point(0, 1, 0)
    half_quarter = transforms.rotation_x(pi / 4)
    full_quarter = transforms.rotation_x(pi / 2)

    assert half_quarter * point == Tuple.point(0, sqrt(2)/2, sqrt(2)/2)
    assert full_quarter * point == Tuple.point(0, 0, 1)


def test_rotation_x_inverse():
    point = Tuple.point(0, 1, 0)
    transform = transforms.rotation_x(pi / 4).inverse()

    assert transform * point == Tuple.point(0, sqrt(2) / 2, -sqrt(2) / 2)


def test_rotation_y():
    point = Tuple.point(0, 0, 1)
    half_quarter = transforms.rotation_y(pi / 4)
    full_quarter = transforms.rotation_y(pi / 2)

    assert half_quarter * point == Tuple.point(sqrt(2)/2, 0, sqrt(2)/2)
    assert full_quarter * point == Tuple.point(1, 0, 0)


def test_rotation_z():
    point = Tuple.point(0, 1, 0)
    half_quarter = transforms.rotation_z(pi / 4)
    full_quarter = transforms.rotation_z(pi / 2)

    assert half_quarter * point == Tuple.point(-sqrt(2)/2, sqrt(2)/2, 0)
    assert full_quarter * point == Tuple.point(-1, 0, 0)


@mark.parametrize(
    "transform, expected",
    (
        (transforms.shearing(1, 0, 0, 0, 0, 0), Tuple.point(5, 3, 4)),
        (transforms.shearing(0, 1, 0, 0, 0, 0), Tuple.point(6, 3, 4)),
        (transforms.shearing(0, 0, 1, 0, 0, 0), Tuple.point(2, 5, 4)),
        (transforms.shearing(0, 0, 0, 1, 0, 0), Tuple.point(2, 7, 4)),
        (transforms.shearing(0, 0, 0, 0, 1, 0), Tuple.point(2, 3, 6)),
        (transforms.shearing(0, 0, 0, 0, 0, 1), Tuple.point(2, 3, 7))
    )
)
def test_shearing(transform, expected):
    assert transform * Tuple.point(2, 3, 4) == expected


def test_applying_transforms_in_sequence():
    point = Tuple.point(1, 0, 1)
    rotation = transforms.rotation_x(pi / 2)
    scaling = transforms.scaling(5, 5, 5)
    translation = transforms.translation(10, 5, 7)

    point = rotation * point
    assert point == Tuple.point(1, -1, 0)

    point = scaling * point
    assert point == Tuple.point(5, -5, 0)

    point = translation * point
    assert point == Tuple.point(15, 0, 7)


def test_chained_transforms():
    point = Tuple.point(1, 0, 1)
    rotation = transforms.rotation_x(pi / 2)
    scaling = transforms.scaling(5, 5, 5)
    translation = transforms.translation(10, 5, 7)

    transform = translation @ scaling @ rotation
    assert transform * point == Tuple.point(15, 0, 7)


def test_chained_transforms_fluent_api():
    point = Tuple.point(1, 0, 1)
    transform = Matrix.identity.rotate(pi / 2).scale(5, 5, 5).translate(10, 5, 7)
    assert transform * point == Tuple.point(15, 0, 7)
