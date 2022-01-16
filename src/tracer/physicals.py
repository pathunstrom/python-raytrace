from __future__ import annotations

from collections import UserList
from dataclasses import dataclass
from math import sqrt
from typing import Protocol, Optional

from .shared import number, EPSILON
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

    def prepare_computations(self, ray) -> Computations:
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
            return sorted((i for i in self if i.distance > 0) , key=lambda x: x.distance)[0]
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

    def lighting(self, light: Light, surface_position: Vector, eye_vector: Vector, surface_normal: Vector, in_shadow: bool = False) -> Color:
        effective_color = self.color * light.intensity
        light_vector = (light.position - surface_position).normalize()

        ambient = effective_color * self.ambient

        light_v_dot_surface_normal = light_vector.dot(surface_normal)

        if light_v_dot_surface_normal < 0 or in_shadow:
            return ambient + black + black

        diffuse = effective_color * self.diffuse * light_v_dot_surface_normal

        reflection_vector = (-light_vector).reflect(surface_normal)
        reflect_dot_eye = reflection_vector.dot(eye_vector)

        if reflect_dot_eye <0:
            return ambient + diffuse + black

        factor = reflect_dot_eye ** self.shininess
        specular = light.intensity * self.specular * factor

        return ambient + diffuse + specular


@dataclass
class AbstractHull:
    transform: Matrix = Matrix.identity
    material: Material = Material()


@dataclass
class Sphere(AbstractHull):
    origin: Vector = Vector.point(0, 0, 0)
    radius: number = 1

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

    def normal_at(self, world_point: Vector) -> Vector:
        object_point = self.transform.inverse() * world_point
        object_space_normal = object_point - self.origin
        x, y, z, _ = self.transform.submatrix(3, 3).inverse().transpose() * object_space_normal
        return Vector(x, y, z, 0).normalize()


@dataclass
class Light:
    position: Vector = Vector.point(0, 0, 0)
    intensity: Color = Color(1, 1, 1)
