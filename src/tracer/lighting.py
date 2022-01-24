from __future__ import annotations

from collections import UserList
from dataclasses import dataclass
from typing import Optional, Protocol

from .shared import EPSILON, number
from .tuples import Vector, Color
from .matrices import Matrix

black = Color(0, 0, 0)


class Hull(Protocol):
    transform: Matrix
    material: Material

    def intersects(self, ray: Ray) -> Intersections[Intersection]:
        ...

    def normal_at(self, point: Vector) -> Vector:
        ...

    def lighting(
            self, light: Light, surface_position: Vector, eye_vector: Vector, surface_normal: Vector,
            in_shadow: bool = False
    ) -> Color:
        ...


class Pattern(Protocol):

    def color_at_hull(self, hull: Hull, point: Vector) -> Color:
        ...


@dataclass
class Computations:
    distance: number
    hull: Hull
    point: Vector
    eye_vector: Vector
    normal_vector: Vector
    over_point: Vector
    inside: bool = False


@dataclass
class Intersection:
    distance: number
    hull: Hull

    def prepare_computations(self, ray: Ray) -> Computations:
        point = ray.position(self.distance)
        eye_vector = -ray.direction
        normal_vector = self.hull.normal_at(point)
        inside = False
        if normal_vector.dot(eye_vector) < 0:
            inside = True
            normal_vector = -normal_vector
        over_point = point + normal_vector * EPSILON

        return Computations(
            self.distance,
            self.hull,
            point,
            eye_vector,
            normal_vector,
            over_point,
            inside
        )


class Intersections(UserList):
    def hit(self) -> Optional[Intersection]:
        try:
            return sorted((i for i in self if i.distance > 0), key=lambda x: x.distance)[0]
        except IndexError:
            return None


@dataclass
class Ray:
    origin: Vector
    direction: Vector

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
class Material:
    color: Color = Color(1, 1, 1)
    ambient: int | float = 0.1
    diffuse: int | float = 0.9
    specular: int | float = 0.9
    shininess: int | float = 200.0
    pattern: Pattern = None


@dataclass
class Light:
    position: Vector = Vector.point(0, 0, 0)
    intensity: Color = Color(1, 1, 1)
