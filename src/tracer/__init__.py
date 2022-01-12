from .shared import *
from .physicals import Intersection, Intersections, Ray, Sphere, Light, Material
from .matrices import Matrix
from .renderer import Canvas
from .tuples import Tuple, Color, ZERO_VECTOR
from .worlds import World
from .cameras import Camera
import tracer.transforms

point = Tuple.point
vector = Tuple.vector
