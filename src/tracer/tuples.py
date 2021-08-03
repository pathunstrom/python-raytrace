from __future__ import annotations

from math import isclose, sqrt
from typing import Union, NamedTuple

from tracer.constants import EPSILON


class Tuple(NamedTuple):
    x: Union[float, int]
    y: Union[float, int]
    z: Union[float, int]
    w: Union[float, int]

    def cross(self, other):
        if self.w != 0 or other.w != 0:
            raise NotImplementedError("Only 3 dimensional cross products supported.")
        return Tuple(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x,
            0
        )

    def dot(self, other):
        return sum(a * b for a, b in zip(self, other))

    @property
    def is_point(self) -> bool:
        return self.w == 1

    @property
    def is_vector(self) -> bool:
        return self.w == 0

    @property
    def magnitude(self) -> Union[float, int]:
        return sqrt(sum(x ** 2 for x in self))

    def normalize(self) -> Tuple:
        magnitude = self.magnitude
        return Tuple(*(v / magnitude for v in self))

    @classmethod
    def point(cls, x, y, z):
        return cls(x, y, z, 1)

    @classmethod
    def vector(cls, x, y, z):
        return cls(x, y, z, 0)

    def __add__(self, other):
        return type(self)(*(left + right for left, right in zip(self, other)))

    def __eq__(self, other):
        return all(isclose(left, right, abs_tol=EPSILON) for left, right in zip(self, other))

    def __mul__(self, scalar):
        return type(self)(*(val * scalar for val in self))

    def __neg__(self):
        return type(self)(*(-x for x in self))

    def __sub__(self, other):
        return type(self)(*(left - right for left, right in zip(self, other)))

    def __truediv__(self, scalar):
        return type(self)(*(val / scalar for val in self))


ZERO_VECTOR = Tuple(0, 0, 0, 0)
