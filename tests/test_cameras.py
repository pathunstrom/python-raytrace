from math import pi, isclose, sqrt

from pytest import mark

from tracer import Camera, Matrix, Ray, point, vector


def test_camera_constructor():
    horizontal_pixels = 160
    vertical_pixels = 120
    field_of_view = pi / 2
    camera = Camera(horizontal_pixels, vertical_pixels, field_of_view)

    assert camera.horizontal_pixels == 160
    assert camera.vertical_pixels == 120
    assert camera.field_of_view == pi / 2
    assert camera.transform == Matrix.identity


@mark.parametrize(
    "horizontal, vertical, expected_pixel_size",
    [
        [200, 125, 0.01],
        [125, 200, 0.01]
    ]
)
def test_camera_pixel_size(horizontal, vertical, expected_pixel_size):
    assert isclose(Camera(horizontal, vertical, pi / 2).pixel_size, expected_pixel_size)


@mark.parametrize(
    "transform, x, y, expected_ray",
    [
        [Matrix.identity, 100, 50, Ray(point(0, 0, 0), vector(0, 0, -1))],
        [Matrix.identity, 0, 0, Ray(point(0, 0, 0), vector(0.66519, 0.33259, -0.66851))],
        [
            Matrix.identity.translate(0, -2, 5).rotate_y(pi / 4),
            100, 50,
            Ray(point(0, 2, -5), vector(sqrt(2) / 2, 0, -(sqrt(2) / 2)))
        ]
    ]
)
def test_camera_ray_for_a_pixel(transform, x, y, expected_ray):
    camera = Camera(201, 101, pi / 2)
    camera.transform = transform
    ray = camera.ray_for_pixel(x, y)
    assert ray == expected_ray
