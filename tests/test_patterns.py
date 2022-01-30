from pytest import mark

from tracer import (
    AbstractPattern,
    CheckeredPattern,
    Color,
    GradientPattern,
    RingPattern,
    SolidPattern,
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
    assert pattern.first_pattern == SolidPattern(color=WHITE)
    assert pattern.second_pattern == SolidPattern(color=BLACK)


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
    pattern = StripePattern(
        first_pattern=SolidPattern(color=WHITE),
        second_pattern=SolidPattern(color=BLACK)
    )
    assert pattern.color_at(input_point) == expected_color


@mark.parametrize(
    "input_point, expected_color",
    [
        [point(0, 0, 0), WHITE],
        [point(0.25, 0, 0), Color(0.75, 0.75, 0.75)],
        [point(0.5, 0, 0), Color(0.5, 0.5, 0.5)],
        [point(0.75, 0, 0), Color(0.25, 0.25, 0.25)]
    ]
)
def test_gradient(input_point: Vector, expected_color: Color):
    pattern = GradientPattern(from_pattern=SolidPattern(color=WHITE), to_pattern=SolidPattern(color=BLACK))
    assert pattern.color_at(input_point) == expected_color


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
    pattern = RingPattern(first_pattern=SolidPattern(color=WHITE), second_pattern=SolidPattern(color=BLACK))
    assert pattern.color_at(input_point) == expected_color


@mark.parametrize(
    "input_point, expected_color",
    [
        [point(0, 0, 0), WHITE],
        [point(0.99, 0, 0), WHITE],
        [point(1.01, 0, 0), BLACK],
        [point(0, 0.99, 0), WHITE],
        [point(0, 1.01, 0), BLACK],
        [point(0, 0, 0.99), WHITE],
        [point(0, 0, 1.01), BLACK]
    ]
)
def test_checker_pattern(input_point, expected_color):
    pattern = CheckeredPattern(first_color=WHITE, second_color=BLACK)
    assert pattern.color_at(input_point) == expected_color


@mark.parametrize(
    "input_point",
    [
        point(0, 1, 0), point(1, 0, 0), point(0.1, 0.1, 0.1), point(0, 0, 1), point(2, 4, 7)
    ]
)
def test_solid_pattern(input_point):
    pattern = SolidPattern(color=WHITE)
    assert pattern.color_at(input_point) == WHITE
