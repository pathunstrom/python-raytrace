from dataclasses import dataclass
from math import floor

from tracer.matrices import Matrix
from tracer.tuples import Color, Vector
from tracer.lighting import Hull


@dataclass
class StripePattern:
    a: Color
    b: Color
    transform: Matrix = Matrix.identity

    def stripe_at(self, point: Vector):
        return self.a if floor(point.x % 2) == 0 else self.b

    def stripe_at_hull(self, hull: Hull, point: Vector):
        local_point = hull.transform.inverse() * point
        pattern_local_point = self.transform.inverse() * local_point
        return self.stripe_at(pattern_local_point)
