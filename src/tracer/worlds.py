from __future__ import annotations
from dataclasses import dataclass, field

from .matrices import Matrix
from .physicals import Light, Hull, Sphere, Material, Intersections, Computations
from .tuples import Tuple, Color


@dataclass
class World:
    children: list[Hull] = field(default_factory=list)
    lights: list[Light] = field(default_factory=list)

    def __len__(self):
        return len(self.children)

    def __contains__(self, item):
        return item in self.children or item in self.lights

    @classmethod
    def default(cls) -> World:
        lights = [Light(Tuple.point(-10, 10, -10), Color(1, 1, 1))]
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
        return World(children, lights)

    def shade_hit(self, computations: Computations) -> Color:
        colors = []
        material = computations.hull.material

        for light in self.lights:
            colors.append(material.lighting(light, computations.point, computations.eye_vector, computations.normal_vector))
        return sum(colors, start=Color(0, 0, 0))

    def intersect(self, ray):
        intersections = []
        for hull in self.children:
            intersections.extend(hull.intersects(ray))
        return Intersections(sorted(intersections, key=lambda x: x.distance))
