from .shared import *
from .physicals import Intersection, Intersections, Ray, Sphere, Light, Material, AbstractHull, Hull, Plane
from .matrices import Matrix
from .patterns import StripePattern
from .renderer import Canvas
from .tuples import Vector, Color, ZERO_VECTOR
from .worlds import World
from .cameras import Camera
import tracer.transforms

point = Vector.point
vector = Vector.vector
