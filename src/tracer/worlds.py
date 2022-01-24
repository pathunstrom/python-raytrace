from __future__ import annotations
from dataclasses import dataclass, field

from .matrices import Matrix
from .physicals import Light, Hull, Sphere, Material, Intersections, Computations, Ray
from .tuples import Vector, Color


@dataclass
class World:
    children: list[Hull] = field(default_factory=list)
    light: Light = None

    def __len__(self):
        return len(self.children)

    def __contains__(self, item):
        return item in self.children or item == self.light

    def color_at(self, ray: Ray) -> Color:
        intersections = self.intersect(ray)
        hit = intersections.hit()
        if not hit:
            return Color(0, 0, 0)
        computations = hit.prepare_computations(ray)
        return self.shade_hit(computations)

    @classmethod
    def default(cls) -> World:
        light = Light(Vector.point(-10, 10, -10), Color(1, 1, 1))
        children = [
            Sphere(
                material=Material(
                    color=Color(0.8, 1.0, 0.6),
                    diffuse=0.7,
                    specular=0.2
                )
            ),
            Sphere(
                transform=Matrix.identity.scale(0.5, 0.5, 0.5)
            )
        ]
        return World(children, light)

    def shade_hit(self, computations: Computations) -> Color:
        hull = computations.hull
        shadowed = self.is_shadowed(computations.over_point)
        return hull.lighting(
            self.light,
            computations.point,
            computations.eye_vector,
            computations.normal_vector,
            shadowed
        )

    def intersect(self, ray) -> Intersections:
        intersections = []
        for hull in self.children:
            intersections.extend(hull.intersects(ray))
        return Intersections(sorted(intersections, key=lambda x: x.distance))

    def is_shadowed(self, point) -> bool:
        to_light = self.light.position - point
        distance = to_light.magnitude
        ray = Ray(point, to_light.normalize())
        intersections = self.intersect(ray)
        hit = intersections.hit()
        if hit is not None and hit.distance < distance:
            return True
        return False
