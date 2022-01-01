from __future__ import annotations
from dataclasses import dataclass
from typing import Protocol

from .tuples import Tuple


class Hull(Protocol):

    def intersects(self, ray: Ray):
        ...


@dataclass
class Ray:
    origin: Tuple
    direction: Tuple

    def position(self, distance):
        return self.origin + self.direction * distance

    def intersects(self, hull: Hull):
        return hull.intersects(self)
