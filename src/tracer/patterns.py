from dataclasses import dataclass
from math import floor

from tracer.tuples import Color, Vector


@dataclass
class StripePattern:
    a: Color
    b: Color

    def stripe_at(self, point: Vector):
        return self.a if floor(point.x % 2) == 0 else self.b
