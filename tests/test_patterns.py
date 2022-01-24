from pytest import mark

from tracer import StripePattern, WHITE, BLACK, point


def test_create_stripe_pattern():
    pattern = StripePattern(WHITE, BLACK)
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
    pattern = StripePattern(WHITE, BLACK)
    assert pattern.stripe_at(input_point) == WHITE


@mark.parametrize(
    "input_point",
    [
        point(0, 0, 0),
        point(0, 0, 1),
        point(0, 0, 2),
    ]
)
def test_stripe_pattern_constant_in_z(input_point):
    pattern = StripePattern(WHITE, BLACK)
    assert pattern.stripe_at(input_point) == WHITE


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
    pattern = StripePattern(WHITE, BLACK)
    assert pattern.stripe_at(input_point) == expected_color
