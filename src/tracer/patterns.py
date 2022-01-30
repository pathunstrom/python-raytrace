from dataclasses import dataclass
from math import floor, sqrt

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


@dataclass
class GradientPattern(AbstractPattern):
    from_color: Color = WHITE
    to_color: Color = BLACK

    def color_at(self, point: Vector) -> Color:
        return self.from_color + (self.to_color - self.from_color) * (point.x - floor(point.x))


@dataclass
class RingPattern(AbstractPattern):
    first_color: Color = WHITE
    second_color: Color = BLACK

    def color_at(self, point: Vector) -> Color:
        if floor(sqrt(point.x ** 2 + point.z ** 2)) % 2 == 0:
            return self.first_color
        return self.second_color


@dataclass
class CheckeredPattern(AbstractPattern):
    first_color: Color = WHITE
    second_color: Color = BLACK

    def color_at(self, point: Vector) -> Color:
        if sum(floor(v) for v in point[:3]) % 2 == 0:
            return self.first_color
        return self.second_color
