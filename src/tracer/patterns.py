from dataclasses import dataclass
from math import floor

from tracer.matrices import Matrix
from tracer.tuples import Color, Vector, WHITE, BLACK
from tracer.lighting import Hull


@dataclass
class AbstractPattern:
    transform: Matrix = Matrix.identity

    def color_at(self, point: Vector) -> Color:
        raise NotImplementedError

    def color_at_hull(self, hull: Hull, point: Vector) -> Color:
        local_point = hull.transform.inverse() * point
        pattern_local_point = self.transform.inverse() * local_point
        return self.color_at(pattern_local_point)


@dataclass
class StripePattern(AbstractPattern):
    a: Color = WHITE
    b: Color = BLACK

    def color_at(self, point: Vector):
        return self.a if floor(point.x % 2) == 0 else self.b
