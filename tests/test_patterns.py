from pytest import fixture


from tracer import Color, StripePattern


@fixture
def black():
    return Color(0, 0, 0)


@fixture
def white():
    return Color(1, 1, 1)


def test_create_stripe_pattern(white, black):
    pattern = StripePattern(white, black)
    assert pattern.a == white
    assert pattern.b == black


def test_stripe_constant_in_y(white, black):
    pass