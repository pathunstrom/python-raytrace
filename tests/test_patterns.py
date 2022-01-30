from pytest import mark

from tracer import (
    AbstractPattern,
    Color,
    GradientPattern,
    RingPattern,
    StripePattern,
    WHITE,
    BLACK,
    Matrix,
    point,
    Sphere,
    transforms,
    Vector
)


class PatternTestable(AbstractPattern):

    def color_at(self, _point) -> Color:
        return Color(*_point[:3])


def test_create_stripe_pattern():
    pattern = StripePattern()
    assert pattern.a == WHITE
    assert pattern.b == BLACK


@mark.parametrize(
    "input_point",
    [
        point(0, 0, 0),
        point(0, 1, 0),
        point(0, 2, 0)
    ]
)
def test_stripe_pattern_constant_in_y(input_point):
    pattern = StripePattern()
    assert pattern.color_at(input_point) == WHITE


@mark.parametrize(
    "input_point",
    [
        point(0, 0, 0),
        point(0, 0, 1),
        point(0, 0, 2),
    ]
)
def test_stripe_pattern_constant_in_z(input_point):
    pattern = StripePattern()
    assert pattern.color_at(input_point) == WHITE


@mark.parametrize(
    "input_point, expected_color",
    [
        [point(0, 0, 0), WHITE],
        [point(0.9, 0, 0), WHITE],
        [point(1, 0, 0), BLACK],
        [point(-0.1, 0, 0), BLACK],
        [point(-1, 0, 0), BLACK],
        [point(-1.1, 0, 0), WHITE]
    ]
)
def test_stripe_pattern_alternates_in_x(input_point, expected_color):
    pattern = StripePattern()
    assert pattern.color_at(input_point) == expected_color


def test_stripes_with_object_transform():
    hull = Sphere(transform=transforms.scaling(2, 2, 2))
    pattern = PatternTestable()
    assert pattern.color_at_hull(hull, point(2, 3, 4)) == Color(1, 1.5, 2)


def test_stripes_with_pattern_transform():
    hull = Sphere()
    pattern = PatternTestable(transforms.scaling(2, 2, 2))
    assert pattern.color_at_hull(hull, point(2, 3, 4)) == Color(1, 1.5, 2)


def test_stripes_with_pattern_and_object_transform():
    hull = Sphere(transform=transforms.scaling(2, 2, 2))
    pattern = PatternTestable(transforms.translation(0.5, 1, 1.5))
    assert pattern.color_at_hull(hull, point(2.5, 3, 3.5)) == Color(0.75, 0.5, 0.25)


def test_abstract_pattern():
    pattern = PatternTestable()
    assert pattern.transform == Matrix.identity


def test_abstract_pattern_with_transform():
    pattern = PatternTestable(transform=transforms.translation(1, 2, 3))
    assert pattern.transform == transforms.translation(1, 2, 3)


def test_abstract_pattern_assign_transform():
    pattern = PatternTestable()
    assert pattern.transform == Matrix.identity
    pattern.transform = transforms.rotation_z(1)
    assert pattern.transform == transforms.rotation_z(1)


@mark.parametrize(
    "point_, color",
    [
        [point(0, 0, 0), WHITE],
        [point(0.25, 0, 0), Color(0.75, 0.75, 0.75)],
        [point(0.5, 0, 0), Color(0.5, 0.5, 0.5)],
        [point(0.75, 0, 0), Color(0.25, 0.25, 0.25)]
    ]
)
def test_gradient(point_: Vector, color: Color):
    pattern = GradientPattern(from_color=WHITE, to_color=BLACK)
    assert pattern.color_at(point_) == color


@mark.parametrize(
    "input_point, expected_color",
    [
        [point(0, 0, 0), WHITE],
        [point(1, 0, 0), BLACK],
        [point(0, 0, 1), BLACK],
        [point(0.708, 0, 0.708), BLACK]
    ]
)
def test_ring_pattern(input_point, expected_color):
    pattern = RingPattern(first_color=WHITE, second_color=BLACK)
    assert pattern.color_at(input_point) == expected_color
