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
class SolidPattern(AbstractPattern):
    color: Color = WHITE

    def color_at(self, point: Vector) -> Color:
        return self.color


@dataclass
class StripePattern(AbstractPattern):
    first_pattern: AbstractPattern = SolidPattern(color=WHITE)
    second_pattern: AbstractPattern = SolidPattern(color=BLACK)

    def color_at(self, point: Vector):
        return self.first_pattern.color_at(point) if floor(point.x % 2) == 0 else self.second_pattern.color_at(point)


@dataclass
class GradientPattern(AbstractPattern):
    from_pattern: AbstractPattern = SolidPattern(color=WHITE)
    to_pattern: AbstractPattern = SolidPattern(color=BLACK)

    def color_at(self, point: Vector) -> Color:
        from_color = self.from_pattern.color_at(point)
        to_color = self.to_pattern.color_at(point)
        print(from_color, to_color)
        return from_color + (to_color - from_color) * (point.x - floor(point.x))


@dataclass
class RingPattern(AbstractPattern):
    first_pattern: AbstractPattern = SolidPattern(color=WHITE)
    second_pattern: AbstractPattern = SolidPattern(color=BLACK)

    def color_at(self, point: Vector) -> Color:
        if floor(sqrt(point.x ** 2 + point.z ** 2)) % 2 == 0:
            return self.first_pattern.color_at(point)
        return self.second_pattern.color_at(point)


@dataclass
class CheckeredPattern(AbstractPattern):
    first_color: Color = WHITE
    second_color: Color = BLACK

    def color_at(self, point: Vector) -> Color:
        if sum(floor(v) for v in point[:3]) % 2 == 0:
            return self.first_color
        return self.second_color
