from tracer import StripePattern, WHITE, BLACK


def test_create_stripe_pattern():
    pattern = StripePattern(WHITE, BLACK)
    assert pattern.a == WHITE
    assert pattern.b == BLACK


def test_stripe_constant_in_y():
    pass
