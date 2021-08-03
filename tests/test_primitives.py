from math import isclose, sqrt

from pytest import mark

from tracer import Tuple, ZERO_VECTOR, EPSILON


@mark.parametrize(
    "x, y, z, w",
    (
        (4.3, -4.2, 3.1, 1.0),
    )
)
def test_tuple_is_point(x, y, z, w):
    point = Tuple(x, y, z, w)
    assert point.w == 1
    assert point.is_point
    assert not point.is_vector


@mark.parametrize(
    "x, y, z, w",
    (
        (4.3, -4.2, 3.1, 0.0),
    )
)
def test_tuple_is_vector(x, y, z, w):
    vector = Tuple(x, y, z, w)
    assert vector.w == 0
    assert not vector.is_point
    assert vector.is_vector


@mark.parametrize(
    "x, y, z",
    (
        (4, -4, 3),
    )
)
def test_tuple_point(x, y, z):
    point = Tuple.point(x, y, z)
    assert point == Tuple(x, y, z, 1)


@mark.parametrize(
    "x, y, z",
    (
        (4, -4, 3),
    )
)
def test_tuple_vector(x, y, z):
    vector = Tuple.vector(x, y, z)
    assert vector == Tuple(x, y, z, 0)


@mark.parametrize(
    "left, right, expected",
    (
        (
            (3, -2, 5, 1),
            (-2, 3, 1, 0),
            (1, 1, 6, 1)
        ),
    )
)
def test_tuple_addition(left, right, expected):
    assert Tuple(*left) + Tuple(*right) == Tuple(*expected)


@mark.parametrize(
    "left, right, expected",
    (
        (
            (3, 2, 1),
            (5, 6, 7),
            (-2, -4, -6)
        ),
    )
)
def test_tuple_subtraction_point_from_point(left, right, expected):
    assert Tuple.point(*left) - Tuple.point(*right) == Tuple.vector(*expected)


def test_tuple_subtraction_vector_from_point():
    assert Tuple.point(3, 2, 1) - Tuple.vector(5, 6, 7) == Tuple.point(-2, -4, -6)


def test_tuple_subtraction_vector_from_vector():
    assert Tuple.vector(3, 2, 1) - Tuple.vector(5, 6, 7) == Tuple.vector(-2, -4, -6)


def test_tuple_subtraction_from_zero_vector():
    assert ZERO_VECTOR - Tuple.vector(1, -2, 3) == Tuple.vector(-1, 2, -3)


def test_tuple_negation():
    a = Tuple(1, -2, 3, -4)
    assert -a == Tuple(-1, 2, -3, 4)


@mark.parametrize(
    "inputs, scalar, expected_values",
    (
        ((1, -2, 3, -4), 3.5, (3.5, -7, 10.5, -14)),
        ((1, -2, 3, -4), 0.5, (0.5, -1, 1.5, -2))
    )
)
def test_tuple_multiply_scalars(inputs, scalar, expected_values):
    assert Tuple(*inputs) * scalar == Tuple(*expected_values)


def test_tuple_divide_scalars():
    assert Tuple(1, -2, 3, -4) / 2 == Tuple(0.5, -1, 1.5, -2)


@mark.parametrize(
    "inputs, expected",
    (
        ((1, 0, 0), 1),
        ((0, 1, 0), 1),
        ((0, 0, 1), 1),
        ((1, 2, 3), sqrt(14)),
        ((-1, -2, -3), sqrt(14))
    )
)
def test_tuple_magnitude(inputs, expected):
    assert isclose(Tuple.vector(*inputs).magnitude, expected, abs_tol=EPSILON)


@mark.parametrize(
    "input, expected",
    (
        ((4, 0, 0), (1, 0, 0)),
        ((1, 2, 3), (0.26726, 0.53452, 0.80178)),
    )
)
def test_tuple_normalize(input, expected):
    normalized = Tuple.vector(*input).normalize()
    assert normalized == Tuple.vector(*expected)
    assert isclose(normalized.magnitude, 1, abs_tol=EPSILON)


def test_tuple_dot_product():
    assert Tuple.vector(1, 2, 3).dot(Tuple.vector(2, 3, 4)) == 20


def test_tuple_cross_product():
    a = Tuple.vector(1, 2, 3)
    b = Tuple.vector(2, 3, 4)
    assert a.cross(b) == Tuple.vector(-1, 2, -1)
    assert b.cross(a) == Tuple.vector(1, -2, 1)
