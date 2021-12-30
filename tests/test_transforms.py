"""
Test tracer transforms.

Transforms are helper methods for creating Matrix objects.
"""
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
