from dataclasses import dataclass


from tracer.tuples import Color


@dataclass
class StripePattern:
    a: Color
    b: Color
