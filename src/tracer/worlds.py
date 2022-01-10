from .physicals import Light
from .tuples import Tuple, Color


class World:

    def __init__(self, *objs, lights=tuple()):
        self.lights = list(lights)
        self.children = list(objs)

    def __len__(self):
        return len(self.children)
