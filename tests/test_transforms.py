"""
Test tracer transforms.

Transforms are helper methods for creating Matrix objects.
"""
from math import pi, sqrt

from pytest import mark

from tracer import transforms, Vector, Matrix, point, vector


def test_translation():
    transform = transforms.translation(5, -3, 2)
    inverse = transform.inverse()
    _point = point(-3, 4, 5)

    assert transform * _point == point(2, 1, 7)
    assert inverse * _point == point(-8, 7, 3)


def test_translation_no_effect_on_vectors():
    transform = transforms.translation(5, -3, 2)
    vector = Vector.vector(-3, 4, 5)

    assert transform * vector == vector


data = [
    (
        transforms.scaling(2, 3, 4),
        Vector.vector(-4, 6, 8),
        Vector.vector(-8, 18, 32)
    ),
    (
        Matrix.identity.scale(2, 3, 4),
        Vector.vector(-4, 6, 8),
        Vector.vector(-8, 18, 32)
    ),
    (
        transforms.scaling(2, 3, 4).inverse(),
        point(-4, 6, 8),
        point(-2, 2, 2)
    ),
    (
        transforms.scaling(2, 3, 4),
        point(-4, 6, 8),
        point(-8, 18, 32)
    ),
    (
        Matrix.identity.scale(2, 3, 4),
        point(-4, 6, 8),
        point(-8, 18, 32)
    ),
    (
        transforms.scaling(-1, 1, 1),
        point(2, 3, 4),
        point(-2, 3, 4)
    ),
    (
        Matrix.identity.scale(-1, 1, 1),
        point(2, 3, 4),
        point(-2, 3, 4)
    ),
    (
        transforms.rotation_x(pi / 4),
        point(0, 1, 0),
        point(0, sqrt(2)/2, sqrt(2)/2)
    ),
    (
        Matrix.identity.rotate_x(pi / 4),
        point(0, 1, 0),
        point(0, sqrt(2) / 2, sqrt(2) / 2)
    ),
    (
        transforms.rotation_x(pi / 2),
        point(0, 1, 0),
        point(0, 0, 1)
    ),
    (
        Matrix.identity.rotate_x(pi / 2),
        point(0, 1, 0),
        point(0, 0, 1)
    ),
    [
        transforms.rotation_y(pi / 4),
        point(0, 0, 1),
        point(sqrt(2)/2, 0, sqrt(2)/2)
    ],
    (
        Matrix.identity.rotate_y(pi / 4),
        point(0, 0, 1),
        point(sqrt(2)/2, 0, sqrt(2)/2)
    ),
    (
        transforms.rotation_y(pi / 2),
        point(0, 0, 1),
        point(1, 0, 0)
    ),
    (
        Matrix.identity.rotate_y(pi / 2),
        point(0, 0, 1),
        point(1, 0, 0)
    ),
    (
        transforms.rotation_z(pi / 4),
        point(0, 1, 0),
        point(-sqrt(2)/2, sqrt(2)/2, 0)
    ),
    (
        transforms.rotation_z(pi / 2),
        point(0, 1, 0),
        point(-1, 0, 0)
    ),
    (
        Matrix.identity.rotate_z(pi / 4),
        point(0, 1, 0),
        point(-sqrt(2)/2, sqrt(2)/2, 0)
    ),
    (
        Matrix.identity.rotate_z(pi / 2),
        point(0, 1, 0),
        point(-1, 0, 0)
    ),
    (
        transforms.rotation_x(pi / 4).inverse(),
        point(0, 1, 0),
        point(0, sqrt(2) / 2, -sqrt(2) / 2)
    )
]


@mark.parametrize("transform,_input,expected", data)
def test_transform(transform, _input: Vector, expected):
    assert transform * _input == expected


@mark.parametrize(
    "transform, expected",
    (
        (transforms.shearing(1, 0, 0, 0, 0, 0), point(5, 3, 4)),
        (transforms.shearing(0, 1, 0, 0, 0, 0), point(6, 3, 4)),
        (transforms.shearing(0, 0, 1, 0, 0, 0), point(2, 5, 4)),
        (transforms.shearing(0, 0, 0, 1, 0, 0), point(2, 7, 4)),
        (transforms.shearing(0, 0, 0, 0, 1, 0), point(2, 3, 6)),
        (transforms.shearing(0, 0, 0, 0, 0, 1), point(2, 3, 7)),
        (Matrix.identity.shear(1, 0, 0, 0, 0, 0), point(5, 3, 4)),
        (Matrix.identity.shear(0, 1, 0, 0, 0, 0), point(6, 3, 4)),
        (Matrix.identity.shear(0, 0, 1, 0, 0, 0), point(2, 5, 4)),
        (Matrix.identity.shear(0, 0, 0, 1, 0, 0), point(2, 7, 4)),
        (Matrix.identity.shear(0, 0, 0, 0, 1, 0), point(2, 3, 6)),
        (Matrix.identity.shear(0, 0, 0, 0, 0, 1), point(2, 3, 7))

    )
)
def test_shearing(transform, expected):
    assert transform * point(2, 3, 4) == expected


def test_applying_transforms_in_sequence():
    _point = point(1, 0, 1)
    rotation = transforms.rotation_x(pi / 2)
    scaling = transforms.scaling(5, 5, 5)
    translation = transforms.translation(10, 5, 7)

    _point = rotation * _point
    assert _point == point(1, -1, 0)

    _point = scaling * _point
    assert _point == point(5, -5, 0)

    _point = translation * _point
    assert _point == point(15, 0, 7)


def test_chained_transforms():
    _point = point(1, 0, 1)
    rotation = transforms.rotation_x(pi / 2)
    scaling = transforms.scaling(5, 5, 5)
    translation = transforms.translation(10, 5, 7)

    transform = translation @ scaling @ rotation
    assert transform * _point == point(15, 0, 7)


def test_chained_transforms_fluent_api():
    _point = point(1, 0, 1)
    transform = Matrix.identity.rotate_x(pi / 2).scale(5, 5, 5).translate(10, 5, 7)
    assert transform * _point == point(15, 0, 7)


@mark.parametrize(
    "from_point, to_point, up_vector, expected_transform",
    [
        [point(0, 0, 0), point(0, 0, -1), vector(0, 1, 0), Matrix.identity],
        [point(0, 0, 0), point(0, 0, 1), vector(0, 1, 0), transforms.scaling(-1, 1, -1)],
        [point(0, 0, 8), point(0, 0, 0), vector(0, 1, 0), transforms.translation(0, 0, -8)],
        [
            point(1, 3, 2),
            point(4, -2, 8),
            vector(1, 1, 0),
            Matrix(
                -0.50709, 0.50709, 0.67612, -2.36643,
                0.76772, 0.60609, 0.12122, -2.82843,
                -0.35857, 0.59761, -0.71714, 0.0,
                0, 0, 0, 1,
            )
        ]
    ]
)
def test_matrix_view(from_point, to_point, up_vector, expected_transform):
    transform = Matrix.view(from_point, to_point, up_vector)
    assert transform == expected_transform
