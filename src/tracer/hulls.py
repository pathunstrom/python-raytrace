from dataclasses import dataclass
from math import sqrt

from .shared import number
from .rays import Ray
from .tuples import Tuple


@dataclass
class Sphere:
    origin: Tuple = Tuple.point(0, 0, 0)
    radius: number = 1

    def intersects(self, ray: Ray):
        sphere_to_ray = ray.origin - self.origin

        a = ray.direction.dot(ray.direction)
        b = 2 * ray.direction.dot(sphere_to_ray)
        c = sphere_to_ray.dot(sphere_to_ray) - 1

        discriminant = b ** 2 - 4 * a * c
        if discriminant < 0:
            return tuple()

        intersection_1 = (-b - sqrt(discriminant)) / (2 * a)
        intersection_2 = (-b + sqrt(discriminant)) / (2 * a)
        return intersection_1, intersection_2
