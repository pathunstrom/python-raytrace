from dataclasses import dataclass
from math import sqrt

from .lighting import (
    Intersection,
    Intersections,
    Light,
    Material,
    Ray
)
from .matrices import Matrix
from .shared import EPSILON, number
from .tuples import (
    BLACK,
    Color,
    Vector
)


__all__ = [
    "AbstractHull",
    "Plane",
    "Sphere",
]


@dataclass
class AbstractHull:
    transform: Matrix = Matrix.identity
    material: Material = Material()

    def _intersects(self, ray: Ray) -> Intersections[Intersection]:
        raise NotImplementedError

    def intersects(self, ray: Ray) -> Intersections:
        return self._intersects(ray.transform(self.transform.inverse()))

    def _normal_at(self, point: Vector) -> Vector:
        raise NotImplementedError

    def normal_at(self, point: Vector) -> Vector:
        local_point = self.transform.inverse() * point
        local_normal = self._normal_at(local_point)
        x, y, z, _ = self.transform.inverse().transpose() * local_normal
        return Vector.vector(x, y, z).normalize()

    def lighting(
            self, light: Light, surface_position: Vector, eye_vector: Vector, surface_normal: Vector,
            in_shadow: bool = False
    ) -> Color:
        if self.material.pattern is not None:
            effective_color = self.material.pattern.color_at_hull(self, surface_position) * light.intensity
        else:
            effective_color = self.material.color * light.intensity

        light_vector = (light.position - surface_position).normalize()

        ambient = effective_color * self.material.ambient

        light_v_dot_surface_normal = light_vector.dot(surface_normal)

        if light_v_dot_surface_normal < 0 or in_shadow:
            return ambient + BLACK + BLACK

        diffuse = effective_color * self.material.diffuse * light_v_dot_surface_normal

        reflection_vector = (-light_vector).reflect(surface_normal)
        reflect_dot_eye = reflection_vector.dot(eye_vector)

        if reflect_dot_eye < 0:
            return ambient + diffuse + BLACK

        factor = reflect_dot_eye ** self.material.shininess
        specular = light.intensity * self.material.specular * factor

        return ambient + diffuse + specular


@dataclass
class Sphere(AbstractHull):
    origin: Vector = Vector.point(0, 0, 0)
    radius: number = 1

    def _intersects(self, ray: Ray) -> Intersections[Intersection]:
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

    def _normal_at(self, object_point: Vector) -> Vector:
        return object_point - self.origin


@dataclass
class Plane(AbstractHull):

    def _intersects(self, ray: Ray) -> Intersections[Intersection]:
        if abs(ray.direction.y) < EPSILON:
            return Intersections()
        return Intersections((Intersection((-ray.origin.y) / ray.direction.y, self),))

    def _normal_at(self, point: Vector) -> Vector:
        return Vector.vector(0, 1, 0)
