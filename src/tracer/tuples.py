from __future__ import annotations

from functools import wraps, singledispatchmethod
from math import isclose, sqrt
from typing import Union, NamedTuple

from tracer.constants import EPSILON


def length_protection(function):

    @wraps(function)
    def wrapper(left, right):
        if len(left) != len(right):
            raise ValueError(f"May only {function.__name__} tuples of the same length.")
        return function(left, right)
    return wrapper


@length_protection
def add(self, other):
    return type(self)(*(left + right for left, right in zip(self, other)))


@length_protection
def subtract(self, other):
    return type(self)(*(left - right for left, right in zip(self, other)))


@length_protection
def compare_equality(self, other):
    return all(isclose(left, right, abs_tol=EPSILON) for left, right in zip(self, other))


def scalar_multiplication(self, scalar):
    return type(self)(*(val * scalar for val in self))


@length_protection
def hadamard_product(self, other):
    return type(self)(*(left * right for left, right in zip(self, other)))


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
        return add(self, other)

    def __eq__(self, other):
        return compare_equality(self, other)

    def __mul__(self, scalar):
        return scalar_multiplication(self, scalar)

    def __neg__(self):
        return type(self)(*(-x for x in self))

    def __sub__(self, other):
        return subtract(self, other)

    def __truediv__(self, scalar):
        return type(self)(*(val / scalar for val in self))


class Color(NamedTuple):
    red: Union[float, int]
    green: Union[float, int]
    blue: Union[float, int]

    def __add__(self, other):
        return add(self, other)

    def __eq__(self, other):
        return compare_equality(self, other)

    def __sub__(self, other):
        return subtract(self, other)

    @singledispatchmethod
    def __mul__(self, other):
        return hadamard_product(self, other)

    @__mul__.register(int)
    @__mul__.register(float)
    def _(self, scalar):
        return scalar_multiplication(self, scalar)


ZERO_VECTOR = Tuple(0, 0, 0, 0)
