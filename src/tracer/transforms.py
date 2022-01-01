from __future__ import annotations

from math import cos, sin
from typing import Union

from .matrices import Matrix

number = Union[float, int]


def translation(x: number, y: number, z: number) -> Matrix:
    return Matrix(
        1, 0, 0, x,
        0, 1, 0, y,
        0, 0, 1, z,
        0, 0, 0, 1
    )


def scaling(x: number, y: number, z: number) -> Matrix:
    return Matrix(
        x, 0, 0, 0,
        0, y, 0, 0,
        0, 0, z, 0,
        0, 0, 0, 1
    )


def rotation_x(radians: number) -> Matrix:
    return Matrix(
        1, 0, 0, 0,
        0, cos(radians), -sin(radians), 0,
        0, sin(radians), cos(radians), 0,
        0, 0, 0, 1
    )


def rotation_y(radians: number) -> Matrix:
    return Matrix(
        cos(radians), 0, sin(radians), 0,
        0, 1, 0, 0,
        -sin(radians), 0, cos(radians), 0,
        0, 0, 0, 1
    )


def rotation_z(radians: number) -> Matrix:
    return Matrix(
        cos(radians), -sin(radians), 0, 0,
        sin(radians), cos(radians), 0, 0,
        0, 0, 1, 0,
        0, 0, 0, 1
    )


def shearing(xy, xz, yx, yz, zx, zy):
    return Matrix(
        1, xy, xz, 0,
        yx, 1, yz, 0,
        zx, zy, 1, 0,
        0, 0, 0, 1
    )
