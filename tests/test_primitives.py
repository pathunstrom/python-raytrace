from math import isclose, sqrt

from pytest import mark, raises

from tracer import Vector, Color, ZERO_VECTOR, EPSILON, point, vector


@mark.parametrize(
    "x, y, z, w",
    (
        (4.3, -4.2, 3.1, 1.0),
    )
)
def test_tuple_is_point(x, y, z, w):
    point = Vector(x, y, z, w)
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
    vector = Vector(x, y, z, w)
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
    _point = point(x, y, z)
    assert _point == Vector(x, y, z, 1)


@mark.parametrize(
    "x, y, z",
    (
        (4, -4, 3),
    )
)
def test_tuple_vector(x, y, z):
    _vector = vector(x, y, z)
    assert _vector == Vector(x, y, z, 0)


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
    assert Vector(*left) + Vector(*right) == Vector(*expected)


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
    assert Vector.point(*left) - Vector.point(*right) == vector(*expected)


def test_tuple_subtraction_vector_from_point():
    assert point(3, 2, 1) - vector(5, 6, 7) == point(-2, -4, -6)


def test_tuple_subtraction_vector_from_vector():
    assert vector(3, 2, 1) - vector(5, 6, 7) == vector(-2, -4, -6)


def test_tuple_subtraction_from_zero_vector():
    assert ZERO_VECTOR - vector(1, -2, 3) == vector(-1, 2, -3)


def test_tuple_negation():
    a = Vector(1, -2, 3, -4)
    assert -a == Vector(-1, 2, -3, 4)


@mark.parametrize(
    "inputs, scalar, expected_values",
    (
        ((1, -2, 3, -4), 3.5, (3.5, -7, 10.5, -14)),
        ((1, -2, 3, -4), 0.5, (0.5, -1, 1.5, -2))
    )
)
def test_tuple_multiply_scalars(inputs, scalar, expected_values):
    assert Vector(*inputs) * scalar == Vector(*expected_values)


def test_tuple_divide_scalars():
    assert Vector(1, -2, 3, -4) / 2 == Vector(0.5, -1, 1.5, -2)


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
    assert isclose(vector(*inputs).magnitude, expected, abs_tol=EPSILON)


@mark.parametrize(
    "input, expected",
    (
        ((4, 0, 0), (1, 0, 0)),
        ((1, 2, 3), (0.26726, 0.53452, 0.80178)),
    )
)
def test_tuple_normalize(input, expected):
    normalized = vector(*input).normalize()
    assert normalized == vector(*expected)
    assert isclose(normalized.magnitude, 1, abs_tol=EPSILON)


def test_tuple_dot_product():
    assert vector(1, 2, 3).dot(vector(2, 3, 4)) == 20


def test_tuple_cross_product():
    a = vector(1, 2, 3)
    b = vector(2, 3, 4)
    assert a.cross(b) == vector(-1, 2, -1)
    assert b.cross(a) == vector(1, -2, 1)


def test_cant_add_color_to_tuple():
    with raises(ValueError):
        value = Color(1, 1, 1) + Vector(2, 3, 4, 5)


def test_cant_subtract_color_from_tuple():
    with raises(ValueError):
        value = Color(1, 1, 1) - Vector(2, 3, 4, 5)


def test_cant_compare_color_and_tuple():
    with raises(ValueError):
        assert Color(1, 1, 1) == Vector(2, 3, 4, 5)


def test_color():
    c = Color(-0.5, 0.4, 1.7)
    assert c.red == -0.5
    assert c.green == 0.4
    assert c.blue == 1.7


def test_color_add():
    assert Color(0.9, 0.6, 0.75) + Color(0.7, 0.1, 0.25) == Color(1.6, 0.7, 1.0)


def test_color_subtract():
    assert Color(0.9, 0.6, 0.75) - Color(0.7, 0.1, 0.25) == Color(0.2, 0.5, 0.5)


def test_color_multiply_by_scalar():
    assert Color(0.2, 0.3, 0.4) * 2 == Color(0.4, 0.6, 0.8)
    assert Color(0.2, 0.3, 0.4) * 0.5 == Color(0.1, 0.15, 0.2)


def test_color_multiply_by_color():
    assert Color(1, 0.2, 0.4) * Color(0.9, 1, 0.1) == Color(0.9, 0.2, 0.04)
