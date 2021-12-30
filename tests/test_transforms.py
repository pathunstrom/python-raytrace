"""
Test tracer transforms.

Transforms are helper methods for creating Matrix objects.
"""
from math import pi, sqrt

from tracer import transforms, Tuple


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
