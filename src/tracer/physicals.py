from __future__ import annotations

from collections import UserList
from dataclasses import dataclass
from math import sqrt
from typing import Protocol

from .shared import number
from .tuples import Tuple


class Hull(Protocol):

    def intersects(self, ray: Ray) -> Intersections[Intersection]:
        ...


@dataclass
class Intersection:
    distance: number
    hull: Hull


class Intersections(UserList):
    pass


@dataclass
class Ray:
    origin: Tuple
    direction: Tuple

    def position(self, distance):
        return self.origin + self.direction * distance

    def intersects(self, hull: Hull):
        return hull.intersects(self)


@dataclass
class Sphere:
    origin: Tuple = Tuple.point(0, 0, 0)
    radius: number = 1

    def intersects(self, ray: Ray) -> Intersections[Intersection]:
        sphere_to_ray = ray.origin - self.origin

        a = ray.direction.dot(ray.direction)
        b = 2 * ray.direction.dot(sphere_to_ray)
        c = sphere_to_ray.dot(sphere_to_ray) - 1

        discriminant = b ** 2 - 4 * a * c
        if discriminant < 0:
            return Intersections()

        intersection_1 = (-b - sqrt(discriminant)) / (2 * a)
        intersection_2 = (-b + sqrt(discriminant)) / (2 * a)

        return Intersections((Intersection(intersection_1, self), Intersection(intersection_2, self)))
