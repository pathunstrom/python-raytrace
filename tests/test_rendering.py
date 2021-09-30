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


def test_save_canvas_headers(tmp_path):
    file_path = tmp_path / "test_file.ppm"
    canvas = Canvas(5, 3)
    canvas.save(file_path)
    with open(file_path) as ppm:
        identifier, size, max_color = (l.strip() for l in ppm.readlines()[:3])
        assert identifier == "P3"
        assert size == "5 3"
        assert max_color == "255"


def test_save_canvas_pixels(tmp_path):
    file_path = tmp_path / "test_file.ppm"
    canvas = Canvas(5, 3)
    color_1 = Color(1.5, 0, 0)
    color_2 = Color(0, 0.5, 0)
    color_3 = Color(-0.5, 0, 1)

    canvas[0, 0] = color_1
    canvas[2, 1] = color_2
    canvas[4, 2] = color_3

    canvas.save(file_path)

    with open(file_path) as ppm:
        pixel_data = ppm.readlines()[3:6]
        expected = """255 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 128 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 255
"""
        assert "".join(pixel_data) == expected


def test_splitting_long_lines_in_ppm(tmp_path):
    test_file_path = tmp_path / "test_file.ppm"
    canvas = Canvas(10, 2, default=Color(1, 0.8, 0.6))
    canvas.save(test_file_path)
    with open(test_file_path) as ppm:
        pixel_data = "".join(ppm.readlines()[3:])
        expected = """255 204 153 255 204 153 255 204 153 255 204 153 255 204 153 255 204
153 255 204 153 255 204 153 255 204 153 255 204 153
255 204 153 255 204 153 255 204 153 255 204 153 255 204 153 255 204
153 255 204 153 255 204 153 255 204 153 255 204 153
"""
        assert pixel_data == expected


def test_ends_with_new_line(tmp_path):
    test_file_path = tmp_path / "test_file.ppm"
    canvas = Canvas(5, 3)
    canvas.save(test_file_path)
    with open(test_file_path) as ppm:
        assert ppm.readlines()[-1].endswith("\n")
