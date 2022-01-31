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
        return self.color_internal(local_point)

    def color_internal(self, point: Vector):
        pattern_local_point = self.transform.inverse() * point
        return self.color_at(pattern_local_point)


@dataclass
class SolidPattern(AbstractPattern):
    color: Color = WHITE

    def color_at_hull(self, hull: Hull, point: Vector) -> Color:
        return self.color

    def color_at(self, point: Vector) -> Color:
        return self.color

    def color_internal(self, point: Vector) -> Color:
        return self.color


@dataclass
class TwoPatternPattern(AbstractPattern):
    first_pattern: AbstractPattern = SolidPattern(color=WHITE)
    second_pattern: AbstractPattern = SolidPattern(color=BLACK)


class StripePattern(TwoPatternPattern):

    def color_at(self, point: Vector):
        if floor(point.x % 2) == 0:
            return self.first_pattern.color_internal(point)
        return self.second_pattern.color_internal(point)


class GradientPattern(TwoPatternPattern):

    def color_at(self, point: Vector) -> Color:
        from_color = self.first_pattern.color_internal(point)
        to_color = self.second_pattern.color_internal(point)
        return from_color + (to_color - from_color) * (point.x - floor(point.x))


class RingPattern(TwoPatternPattern):

    def color_at(self, point: Vector) -> Color:
        if floor(sqrt(point.x ** 2 + point.z ** 2)) % 2 == 0:
            return self.first_pattern.color_internal(point)
        return self.second_pattern.color_internal(point)


class CheckeredPattern(TwoPatternPattern):

    def color_at(self, point: Vector) -> Color:
        v = sum(floor(v) for v in point[:3])
        if v % 2 == 0:
            return self.first_pattern.color_internal(point)
        return self.second_pattern.color_internal(point)


class RadialGradientPattern(TwoPatternPattern):

    def color_at(self, point: Vector) -> Color:
        from_color = self.first_pattern.color_internal(point)
        to_color = self.second_pattern.color_internal(point)
        distance = sqrt(point.x ** 2 + point.z ** 2)
        return from_color + (to_color - from_color) * (distance - floor(distance))


class BlendPattern(TwoPatternPattern):

    def _blend(self, first_color, second_color) -> Color:
        raise NotImplementedError

    def color_at(self, point: Vector) -> Color:
        first_color = self.first_pattern.color_internal(point)
        second_color = self.second_pattern.color_internal(point)
        return self._blend(first_color, second_color)


class AddBlendPattern(BlendPattern):

    def _blend(self, first_color, second_color) -> Color:
        return first_color + second_color


class MultiplyBlendPattern(BlendPattern):

    def _blend(self, first_color, second_color) -> Color:
        return first_color * second_color


class ScreenBlendPattern(BlendPattern):

    def _blend(self, first_color, second_color) -> Color:
        return WHITE - (WHITE - first_color) * (WHITE - second_color)


class AverageBlendPattern(BlendPattern):

    def _blend(self, first_color, second_color) -> Color:
        r = (first_color.red + second_color.red) / 2
        g = (first_color.green + second_color.green) / 2
        b = (first_color.blue + second_color.blue) / 2
        return Color(r, g, b)
