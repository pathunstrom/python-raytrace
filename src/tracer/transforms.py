from __future__ import annotations

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
