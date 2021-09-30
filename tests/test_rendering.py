from tracer import Canvas, Color

black = Color(0, 0, 0)
red = Color(1, 0, 0)


def test_create_canvas():
    canvas = Canvas(10, 20)
    assert canvas.width == 10
    assert canvas.height == 20
    for pixel in canvas:
        assert pixel == black


def test_set_pixel():
    canvas = Canvas(10, 20)
    canvas[2, 3] = red
    assert canvas[(2, 3)] == red
