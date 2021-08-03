from math import isclose
from typing import Union, NamedTuple

from tracer.constants import EPSILON


class Tuple(NamedTuple):
    x: Union[float, int]
    y: Union[float, int]
    z: Union[float, int]
    w: Union[float, int]

    @property
    def is_point(self) -> bool:
        return self.w == 1

    @property
    def is_vector(self) -> bool:
        return self.w == 0

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

    def __neg__(self):
        return type(self)(*(-x for x in self))

    def __sub__(self, other):
        return type(self)(*(left - right for left, right in zip(self, other)))


ZERO_VECTOR = Tuple(0, 0, 0, 0)
