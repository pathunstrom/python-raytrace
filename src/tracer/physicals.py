from __future__ import annotations

from collections import UserList
from dataclasses import dataclass
from math import sqrt
from typing import Protocol, Optional

from .shared import number
from .tuples import Tuple
from .matrices import Matrix


class Hull(Protocol):

    def intersects(self, ray: Ray) -> Intersections[Intersection]:
        ...


@dataclass
class Intersection:
    distance: number
    hull: Hull


class Intersections(UserList):
    def hit(self) -> Optional[Intersection]:
        try:
            return sorted((i for i in self if i.distance > 0) , key=lambda x: x.distance)[0]
        except IndexError:
            return None


@dataclass
class Ray:
    origin: Tuple
    direction: Tuple

    def position(self, distance):
        return self.origin + self.direction * distance

    def intersects(self, hull: Hull):
        return hull.intersects(self)

    def transform(self, transform: Matrix) -> Ray:
        return Ray(
            transform * self.origin,
            transform * self.direction
        )


@dataclass
class Sphere:
    origin: Tuple = Tuple.point(0, 0, 0)
    radius: number = 1
    transform: Matrix = Matrix.identity

    def intersects(self, ray: Ray) -> Intersections[Intersection]:
        ray = ray.transform(self.transform.inverse())

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

    def normal_at(self, world_point: Tuple) -> Tuple:
        object_point = self.transform.inverse() * world_point
        object_space_normal = object_point - self.origin
        x, y, z, _ = self.transform.submatrix(3, 3).inverse().transpose() * object_space_normal
        return Tuple(x, y, z, 0).normalize()
